import {writeMsg} from "./customLog.js";

const editableCellAttributes = (data, row, col) => {
    if (row) {
        return {contentEditable: 'true', 'data-element-id': row.cells[0].data};
    } else {
        return {};
    }
};

async function getFullDatasetByName(name, api_url) {
    let host_url = 'http://localhost:5000'
    let request_url = host_url + api_url + '?' + new URLSearchParams({db_name: name});
    console.log(request_url);
    let response = await fetch(request_url);
    return await response.json()
}

import {
    Grid,
    h
} from "./gridjs.js";

export async function getPreparedDatasetByName(name, api_url, prepareBool) {
    const dataset = await getFullDatasetByName(name, api_url);
    try {
        if (prepareBool) {
            for (const prop in dataset.columns) {
                dataset.columns[prop]['attributes'] = editableCellAttributes;
            }
            dataset.columns.push(
                {
                    name: 'Действия',
                    formatter: (cell, row) => {
                        return h('button', {
                            className: 'btn btn-secondary',
                            onClick: async (ev) => {
                                let delete_url = '/api/delete_row'
                                console.log(currentDatasetName);
                                console.log(ev.target.dataset.elementId);
                                try {
                                    const response = await fetch(delete_url, {
                                            method: 'POST',
                                            headers: {'Content-Type': 'application/json'},
                                            body: JSON.stringify({
                                                id: row.cells[0].data,
                                                table_name: currentDatasetName
                                            }),
                                        }
                                    );
                                    response.status === 200 ? writeMsg(await response.text(), 0): writeMsg(await response.text(), 1);
                                } catch (err) {
                                    writeMsg(err, 2)
                                }

                            }
                        }, 'Удалить');
                    }
                }
            );
        } else return dataset
        return dataset
    } catch (ex) {
        console.log(ex)
        return dataset
    }
}

