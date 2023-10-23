
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
    // 1. ������ ����� XMLHttpRequest-������
        let xhr = new XMLHttpRequest();
        var mode = document.getElementById("isFinal").checked;
    let obj = {
        listcity: placeList,
        mode:mode
            };
    let json = JSON.stringify(obj);
    // 2. ����������� ���: GET-������ �� URL /article/.../load
    xhr.open('POST', 'http://127.0.0.1:8000/items');
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type', 'application/json');
    // 3. �������� ������
    xhr.send(json);

    // 4. ���� ��� ��������� ����� ����, ��� �� ������� ����� �������
    xhr.onload = function () {
                if (xhr.response == 'somethingWrong') { // ����������� HTTP-������ ������, ���� ������ �� 200, �� ��������� ������
                    document.getElementsByClassName("res")[0].innerHTML=`sorry,try again`; // ��������, 404: Not Found
                } else { // ���� �� ������ ������, ������� ���������
                    //location.href = xhr.response; // response -- ��� ����� �������
                    //window.location.assign(xhr.response);
                    chrome.tabs.create({ url: xhr.response });
                    document.getElementsByClassName("res")[0].innerHTML = `<a href="${xhr.response}">route</a>`;
                }
        };
        document.getElementById('submitButton').addEventListener("click", openMap);
        }