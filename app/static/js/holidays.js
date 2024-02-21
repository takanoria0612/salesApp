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