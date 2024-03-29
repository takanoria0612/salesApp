
// 祝日データをフェッチする非同期関数
export async function fetchHolidays() {
    try {
        const response = await fetch('https://holidays-jp.github.io/api/v1/date.json');
        if (!response.ok) {
            throw new Error('Failed to fetch holidays');
        }
        const holidays = await response.json();
        return holidays;
    } catch (error) {
        console.error('fetchHolidays error:', error);
        throw error; 
    }
}

// 前営業日を計算する関数
export function calculateLastBusinessDay(holidays) {
    let date = new Date();
    date.setDate(date.getDate() - 1); // 昨日に設定
    const formatDate = (date) => date.toISOString().split('T')[0];

    while (formatDate(date) in holidays || date.getDay() === 0 || date.getDay() === 6) {
        date.setDate(date.getDate() - 1); // さらに1日遡る
    }

    return formatDate(date); // YYYY-MM-DD形式にフォーマット
}
// その月の営業日数を計算する関数
export async function calculateBusinessDays(year, month) {
    const holidays = await fetchHolidays();
    let businessDays = 0;
    const date = new Date(year, month - 1, 1); // 指定された月の最初の日
    const lastDay = new Date(year, month, 0).getDate(); // 指定された月の最後の日

    while (date.getDate() <= lastDay) {
        const dayOfWeek = date.getDay();
        const formattedDate = date.toISOString().split('T')[0];
        if (dayOfWeek !== 0 && dayOfWeek !== 6 && !(formattedDate in holidays)) {
            businessDays++;
        }
        date.setDate(date.getDate() + 1); // 次の日へ
    }

    return businessDays;
}
