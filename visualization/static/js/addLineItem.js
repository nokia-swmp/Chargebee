function showSubscription(obj) {
    subs = document.getElementById("subs")
    for(i=0; i < subs.length; i++){
        if(subs[i].id != obj.value){
            subs[i].disabled = true;
        }
        else {
            subs[i].disabled = false;
            subs[i].selected = 'selected'
        }
    }
    
}
/*
$("#saveLineItem").click(function(){
    $.ajax({
        method: "POST",
        url: ,
        data: {
            'cust' : document.getElementById("custs").value,
            'subs' : document.getElementById("subs").value,
            'start' : document.getElementById("start").value,
            'end' : document.getElementById("end").value,             
        },
        dataType: "application/json",
        success: function(result){
            //var data=JSON.parse(result);
            console.log(result);
        }
    });
});*/