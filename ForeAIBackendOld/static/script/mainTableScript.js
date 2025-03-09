import ru from "./mylang.js";
import {getPreparedDatasetByName} from "./gridjsPreparation.js";
import {writeMsg} from "./customLog.js";
import {saveValue, enterVal, updateSaved, downloadButtonOnClick} from "./gridjsCustomEvents.js";

const tableDiv = document.getElementById('table');
const downloadDatasetButton = document.getElementById('export-btn');

const updateUrl = (prev, query) => {
    return prev + (prev.indexOf('?') >= 0 ? '&' : '?') + new URLSearchParams(query).toString();
};

const dataset = await getPreparedDatasetByName(testName, apiAdr, prepareBool);

const mygrid = new gridjs.Grid({
    columns: dataset.columns,
    data: dataset.data,
    search: true,
    sort: {
        enabled: true,
        multiColumn: true,
    },
    pagination: true,
    language: ru
}).render(tableDiv);

// если делать пагинацию
// let columnIds = Object.keys(mygrid.config.pagination);

// Загрузка текущего датасета
downloadDatasetButton.addEventListener('click', downloadButtonOnClick);

tableDiv.addEventListener('focusin', saveValue);
tableDiv.addEventListener('focusout', updateSaved);
tableDiv.customApi = customApi;

tableDiv.addEventListener('keydown', enterVal);

const db_select = document.querySelector('#database-name-option');
db_select.addEventListener("change", updateGridJS);

async function updateGridJS(event) {
    let datasetName = event.target.value;
    currentDatasetName = datasetName;
    let dataset = await getPreparedDatasetByName(datasetName, apiAdr, prepareBool);
    writeMsg(`получил данные: ${datasetName}`, 0);
    await mygrid.updateConfig({
        columns: dataset.columns,
        data: dataset.data
    }).forceRender();
}