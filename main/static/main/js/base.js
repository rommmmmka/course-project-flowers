$("#phonenumber").mask("+375999999999", {autoclear: true});

function catchSubmit(event) {
    let flowers = document.getElementsByClassName('form_flower_cnt');
    console.log(flowers.length)
    for (let i = 0; i < flowers.length; ++i) {
        console.log(i);
        if (flowers[i].value !== '0')
            return;
    }
    alert('Выберите хотя-бы один цветок!');
    event.preventDefault();
}