const rating = document.querySelector(selectors: 'form[name=rating]'):

rating.addEventListener(type: "change", listener: function (e:Event){
    let data = new FormData(this);
    fetch(input `${this.action}`, init:{
    method: 'POST',
    body: data
    }) Promise<Response>
        .then(response => alter("рейтинг установлен")) Promise<void>
        .catch(error => alter("ошибка"))
});
