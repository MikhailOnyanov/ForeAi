export default {
    search: {
        placeholder: 'Введите слово для фильтра...',
    },
    sort: {
        sortAsc: 'По возрастанию',
        sortDesc: 'По убыванию',
    },
    pagination: {
        previous: 'Предыдущая',
        next: 'Следующая',
        navigate: (page, pages) => `Страница ${page} из ${pages}`,
        page: (page) => `Страница ${page}`,
        showing: 'Отображается от',
        of: 'из',
        to: 'до',
        results: 'записей',
    },
    loading: 'Загрузка...',
    noRecordsFound: 'Не найдено подходящих записей',
    error: 'Возникла ошибка при загрузке данных',
};