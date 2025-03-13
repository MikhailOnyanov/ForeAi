import {ProcessDocumentationButtonOnClick, downloadOnClick} from "./docButtonsEvents.js";

const processDocumentationButton = document.getElementById('start-processing-btn');
processDocumentationButton.addEventListener('click', ProcessDocumentationButtonOnClick);

const downloadJsonResponseButton = document.getElementById('export-btn');
downloadJsonResponseButton.addEventListener('click', downloadOnClick);