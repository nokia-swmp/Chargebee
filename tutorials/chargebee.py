from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache

from swordfish_app.models import ChargeBeeData
import chargebee
import logging

LOG = logging.getLogger(__name__)

CHARGEBEE_CONFIGURED = False
CHARGEBEE_CACHE_SUBSCRIPTION = "chargebee_subscription_for_%s"
CHARGEBEE_CACHE_PLAN = "chargebee_plan_for_%s"
CHARGEBEE_CACHE_COUPON = "chargebee_coupon_%s"
CHARGEBEE_CACHE_AVAILABLE_PLANS = "chargebee_available_plans"

INVOICE_STATUS_PAID = "paid"
INVOICE_STATUS_PAYMENT_DUE = "payment_due"


class NoPlanSelectedException(Exception):
    pass


def configure_chargebee(reset=False):
    global CHARGEBEE_CONFIGURED

    if reset:
        CHARGEBEE_CONFIGURED = False
        return

    if not CHARGEBEE_CONFIGURED:
        chargebee.configure(settings.CHARGEBEE_APIKEY, settings.CHARGEBEE_SITENAME)
        CHARGEBEE_CONFIGURED = True


def get_customer_id(user):
    try:
        chargebee_customer_id = ChargeBeeData.objects.get(user=user).customer_id

        LOG.debug("Found existing ChargeBee customer_id: %s", chargebee_customer_id)

        return chargebee_customer_id

        # verify existence in chargebee   ???  Not yet. Should be in sync. Don't delete from Chargebee without
        # associated delete in Sf db.

    except ChargeBeeData.DoesNotExist:
        configure_chargebee()

        LOG.debug("chargebee data doesn't exist in Swordfish for user %s" % user)

        data = {
            "first_name": "%s" % user.first_name,
            "last_name": "%s" % user.last_name,
            "email": user.email,
            "auto_collection": "off",
        }
        LOG.debug("CHARGEBEE API CALL - chargebee.Customer.create")
        result = chargebee.Customer.create(data)

        ChargeBeeData.objects.create(user=user, customer_id=result.customer.id)

        LOG.debug("New customer created in ChargeBee [%s] for user [%s].", result.customer.id, user)

        _auto_enroll_user(user, result.customer.id)

        return result.customer.id


def get_current_subscription(user, customer_id=None):
    configure_chargebee()

    customer_id = customer_id if customer_id else get_customer_id(user)

    subscription, plan = \
        cache.get(CHARGEBEE_CACHE_SUBSCRIPTION % user.id), \
        cache.get(CHARGEBEE_CACHE_PLAN % user.id)

    if subscription is None or plan is None:
        LOG.debug("No cached subscription/plan. Fetching from Chargebee API.")

        LOG.debug("CHARGEBEE API CALL - chargebee.Subscription.list")
        subscriptions = chargebee.Subscription.list({
            "limit": 5,
            "customer_id[is]": customer_id,
            "status[is]": "active"
        })

        LOG.debug("Found subscriptions for %s - %s", customer_id, subscriptions)

        if subscriptions:
            subscription = subscriptions[0].subscription

            plan = chargebee.Plan.retrieve(subscription.plan_id).plan

            subscription.name = plan.name

            if settings.CHARGEBEE_CACHE_ELEMENTS:
                cache.set(CHARGEBEE_CACHE_SUBSCRIPTION % user.id, subscription, 30)
                cache.set(CHARGEBEE_CACHE_PLAN % user.id, plan, 30)
    else:
        LOG.debug("Cache HIT for CHARGEBEE_CACHE_SUBSCRIPTION and CHARGEBEE_CACHE_PLAN!! YAY!")

    return subscription, plan


def get_available_plans(filter_by_name=None):
    configure_chargebee()

    plans = cache.get('%s.%s' % (CHARGEBEE_CACHE_AVAILABLE_PLANS, filter_by_name))

    if plans is None:
        LOG.debug("No cached available plans. Fetching from Chargebee API.")
        LOG.debug("CHARGEBEE API CALL - chargebee.Plan.list")

        call_kwargs = {
            "status[is]": "active"
        }
        if filter_by_name:
            call_kwargs['name[is]'] = filter_by_name

        plans = chargebee.Plan.list(call_kwargs)

        if settings.CHARGEBEE_CACHE_ELEMENTS:
            cache.set('%s.%s' % (CHARGEBEE_CACHE_AVAILABLE_PLANS, filter_by_name), plans, 30)
    else:
        LOG.debug("Cache HIT for CHARGEBEE_CACHE_AVAILABLE_PLANS!! YAY!")

    return [_.plan for _ in plans] if len(plans) > 1 else plans[0] if plans else []


def subscribe_using_coupon(customer_id, plan_id, coupon_code):
    configure_chargebee()

    return chargebee.Subscription.create_for_customer(
        customer_id,
        {
            "plan_id": plan_id,
            "invoice_immediately": True,
            "coupon_ids": [coupon_code]
        }
    )


def _auto_enroll_user(user, customer_id):
    # auto subscribe the new customer to the appropriate plan (standard or premium).
    plan_id, coupon_code = "basic-demo-access", "ASTANDARDCOUPON"

    try:
        if Group.objects.get(name="sf_sales") in user.groups.all():
            plan_id, coupon_code = "premium", "premium_coupon"
    except Group.DoesNotExist:
        LOG.debug("Attempted to retrieve sf_sales group. Does not exist.")

    subscribe_using_coupon(customer_id, plan_id, coupon_code)


def get_allowed_instance_count(user, customer_id=None, plan=None):
    try:
        return get_plan_attribute(user, 'max_demos', customer_id, plan)
    except NoPlanSelectedException:
        return settings.MAX_INSTANCE_COUNT_CONFIG_DEFAULT


def get_demo_runtime(user, customer_id=None, plan=None):
    try:
        return get_plan_attribute(user, 'demo_runtime_in_days', customer_id, plan)
    except NoPlanSelectedException:
        return settings.INSTANCE_REAPER_CONFIG_DEFAULT[0]


def get_plan_attribute(user, attribute_name, customer_id=None, plan=None):
    if plan is None:
        customer_id = customer_id or get_customer_id(user)
        _, plan = get_current_subscription(user, customer_id=customer_id)

    if plan:
        return plan.meta_data[attribute_name]
    else:
        raise NoPlanSelectedException("No plan assigned to Sf user %s (Chargebee Customer %s)" % (user, customer_id))


def coupon_retrieve(coupon_code):
    configure_chargebee()

    coupon = cache.get(CHARGEBEE_CACHE_COUPON % coupon_code)

    if coupon is None:
        coupon = chargebee.Coupon.retrieve(coupon_code).coupon
        if settings.CHARGEBEE_CACHE_ELEMENTS:
            cache.set(CHARGEBEE_CACHE_COUPON % coupon_code, coupon, 30)

    return coupon


def subscription_cancel(subscription):
    configure_chargebee()

    chargebee.Subscription.cancel(subscription.id)


def get_outstanding_invoices(user):
    configure_chargebee()

    id = get_customer_id(user)

    LOG.debug("CHARGEBEE API CALL - chargebee.Invoice.list")
    invoices = chargebee.Invoice.list({
        "limit": 5,
        "customer_id[is]": id,
        "status[is]": "payment_due"
    })

    LOG.debug("invoices - %s", invoices)

    if invoices:
        return invoices
    else:
        return []


def cancel_invoices(invoices):
    configure_chargebee()

    for i in invoices:
        chargebee.Invoice.void_invoice(i.invoice.id)


def downgrade_to_standard_plan(user):
    configure_chargebee()

    id = get_customer_id(user)

    subscription, _ = get_current_subscription(user, id)

    subscription_cancel(subscription)
    subscribe_using_coupon(id, get_available_plans('standard').plan.id, 'ASTANDARDCOUPON')


def reset_cache(user, clear_subscription=True, clear_plan=True):
    if settings.CHARGEBEE_CACHE_ELEMENTS:
        if clear_subscription:
            cache.delete(CHARGEBEE_CACHE_SUBSCRIPTION % user.id)
        if clear_plan:
            cache.delete(CHARGEBEE_CACHE_PLAN % user.id)
    else:
        LOG.debug("reset_cache - CHARGEBEE_CACHE_ELEMENTS is False, nothing to do...")