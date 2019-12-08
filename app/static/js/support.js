function ru_date(s_date) {
    let ru_months = ['января', 'февраля', 'марта',
                 'апреля', 'мая', 'июня',
                 'июля', 'августа', 'сентября',
                 'октября', 'ноября', 'декабря']

    let year = Number(s_date.slice(0,4));
    let month = ru_months[Number(s_date.slice(5,7))-1];
    let day = Number(s_date.slice(8,10));

    return `${day} ${month} ${year}г.`
};