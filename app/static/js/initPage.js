// initPage.js
import { fetchHolidays, calculateLastBusinessDay } from './holidays.js';
import { updateFormData } from './formUtils.js'; // 仮の関数名、formUtils.jsに実装される想定
import { showBootstrapAlert } from './dateHandlers.js';
let holidays = {}; // 祝日データを格納するグローバル変数

export async function initPage() {
    try {
        holidays = await fetchHolidays();
        const businessDay = calculateLastBusinessDay(holidays);
        document.getElementById('date').value = businessDay;

        const response = await fetch('/set-business-day', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ businessDay: businessDay }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        if (data.status === 'success') {
            updateFormData(data.data); // フォームの値を更新する関数
        } else {
            showBootstrapAlert('warning', 'データがありませ!ん。');;
            if (data.message) {
                showBootstrapAlert(data.message);

            }
        }
    } catch (error) {
        console.error('Error fetching or processing holidays:', error);
        showBootstrapAlert('error','祝日データの取得に失敗しました。');
    }
}

window.onload = initPage;