import {writeMsg} from "./customLog.js";

export async function ProcessDocumentationButtonOnClick(ev) {
    console.log('clicked process button!')
    let host_url = 'http://localhost:5000'
    let request_url = host_url + processDocumentationApiAdr
    console.log(request_url);
    writeMsg(`Послал запрос на обработку документации: ${host_url}`, 0);
    let response = await fetch(request_url, {
        method: "POST",
        body: JSON.stringify({}),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
    let resp_text = decodeURIComponent(await response.text());
    writeMsg(`Полученный текст справки: ${resp_text}`, 0);
    console.log(resp_text);
    resultJson = resp_text;
}

export async function downloadOnClick(ev) {
    let fileName = "result.json";
    let contentType="json";
    console.log("в загрузке я");
    if (resultJson == null) {
        console.log("нет результата ещё")
    } else {
        var a = document.createElement("a");
        var file = new Blob([resultJson], {type: contentType});
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
    }
}