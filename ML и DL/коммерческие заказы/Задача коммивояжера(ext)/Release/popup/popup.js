
document.getElementById('newCityDivButton').addEventListener("click", newCityDiv);
document.getElementById('submitButton').addEventListener("click", openMap);

    var id = 1;
    var cities = '';
    function newCityDiv() {
        document.getElementsByClassName("cityList")[0].innerHTML +=
        `<div class="cityDiv" id=city${id}>
               <input type="text" class="city">
           </div>`;
        document.getElementById('newCityDivButton').addEventListener("click", newCityDiv);
    id++;
        };
    function openMap() {
        let placeList = Array.from(document.querySelectorAll('input')).map(inputElement => inputElement.value);
        placeList.pop();
    // 1. Создаём новый XMLHttpRequest-объект
        let xhr = new XMLHttpRequest();
        var mode = document.getElementById("isFinal").checked;
    let obj = {
        listcity: placeList,
        mode:mode
            };
    let json = JSON.stringify(obj);
    // 2. Настраиваем его: GET-запрос по URL /article/.../load
    xhr.open('POST', 'http://127.0.0.1:8000/items');
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type', 'application/json');
    // 3. Отсылаем запрос
    xhr.send(json);

    // 4. Этот код сработает после того, как мы получим ответ сервера
    xhr.onload = function () {
                if (xhr.response == 'somethingWrong') { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
                    document.getElementsByClassName("res")[0].innerHTML=`sorry,try again`; // Например, 404: Not Found
                } else { // если всё прошло гладко, выводим результат
                    //location.href = xhr.response; // response -- это ответ сервера
                    //window.location.assign(xhr.response);
                    chrome.tabs.create({ url: xhr.response });
                    document.getElementsByClassName("res")[0].innerHTML = `<a href="${xhr.response}">route</a>`;
                }
        };
        document.getElementById('submitButton').addEventListener("click", openMap);
        }