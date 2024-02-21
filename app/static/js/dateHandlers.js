import { setFormReadOnly, clearFormData, updateFinancials } from './formUtils.js';
import { fetchHolidays } from './holidays.js';
export async function fetchDataForDate(selectedDate) {
    try {
        const response = await fetch(`/fetch-data-for-date?date=${selectedDate}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        if (data.exists) {

            console.log(data, 'yeahhh')
            // データが存在する場合、フォームのフィールドを更新
            document.getElementById('sets').value = data.sets || '';
            document.getElementById('customers').value = data.customers || '';
            document.getElementById('bowls').value = data.bowls || '';
            document.getElementById('purchase_total').value = data.purchase_total || '';
            document.getElementById('total_price').value = data.total_price || '';
            document.getElementById('cash_total').value = data.cash_total || '';
            document.getElementById('card_total').value = data.card_total || '';
            document.getElementById('usd_total').value = data.usd_total || '';
            document.getElementById('remarks').value = data.remarks || '';
            // 他の必要なフィールドも同様に更新
        } else {
            // データが存在しない場合の処理（例：フォームをクリア）
            clearFormData();
            alert('データがありません。');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('データの取得に失敗しました。');
    }
}

// グローバル変数として定義
let holidays = {};

// アプリケーションの初期化または適切なタイミングで祝日データをフェッチ
async function initializeHolidays() {
    try {
        holidays = await fetchHolidays();
    } catch (error) {
        console.error('Failed to fetch holidays:', error);
    }
}

    // 日付変更時の処理を行う関数
export async function handleDateChange(event) {
    const selectedDate = event.target.value;
    const date = new Date(selectedDate);
    const dayOfWeek = date.getDay();

    if (dayOfWeek === 0 || dayOfWeek === 6) {
        alert('土、日は営業日ではありません。');
        clearFormData();
        setFormReadOnly(true);
    } else if (holidays[selectedDate]) {
        alert('祝日なのでデータの追加ができません');
        clearFormData();
        setFormReadOnly(true);
    } else {
        setFormReadOnly(false);
        try {
            const data = await fetch(`/fetch-data-for-date?date=${selectedDate}`).then(response => response.json());
            if (!data.exists) {
                clearFormData();
                alert('データがありません。');
            } else {
                // document.getElementById('sets').value = data.sets || '';
                // document.getElementById('customers').value = data.customers || '';
                await fetchDataForDate(selectedDate)
            }
        } catch (error) {
            console.error('Error:', error);
            alert('データの取得に失敗しました。');
        }
    }
}
// 初期化関数を実行して祝日データをセット
initializeHolidays();