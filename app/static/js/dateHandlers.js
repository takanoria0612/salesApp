// app/rotues/dateHandlers.js
import { setFormReadOnly, clearFormData, updateFinancials } from './formUtils.js';
import { fetchHolidays } from './holidays.js';



export async function showBootstrapAlert(type, message) {
    const alertPlaceholder = document.getElementById('alert-placeholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
        `   <strong>${message}</strong>`,
        '   <button type="button" class="close" data-dismiss="alert" aria-label="Close">',
        '       <span aria-hidden="true">&times;</span>',
        '   </button>',
        '</div>'
    ].join('');

    alertPlaceholder.appendChild(wrapper);
}
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
            // データが存在しない場合の処理
            clearFormData();
            showBootstrapAlert('warning', 'データがありませんよ');

        }
    } catch (error) {
        console.error('Error:', error);
        showBootstrapAlert('データの取得に失敗しました。');
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
    //　ここでadd.htmlに遷移したとき、データがなければポップアップはく。
export async function handleDateChange(event) {
    const selectedDate = event.target.value;
    const date = new Date(selectedDate);
    const dayOfWeek = date.getDay();

    if (dayOfWeek === 0 || dayOfWeek === 6) {
        showBootstrapAlert('warning', '土、日は営業日ではありません。');
        clearFormData();
        setFormReadOnly(true);
    } else if (holidays[selectedDate]) {
        showBootstrapAlert('warning', '祝日なのでデータの追加ができません');
        clearFormData();
        setFormReadOnly(true);
    } else {
        setFormReadOnly(false);
        try {
            const data = await fetch(`/fetch-data-for-date?date=${selectedDate}`).then(response => response.json());
            if (!data.exists) {
                clearFormData();
                showBootstrapAlert('warning', 'データがありません。');
            } else {
                // document.getElementById('sets').value = data.sets || '';
                // document.getElementById('customers').value = data.customers || '';
                await fetchDataForDate(selectedDate)
            }
        } catch (error) {
            console.error('Error:', error);
            showBootstrapAlert('error', 'データの取得に失敗しました。');
        }
    }
}
// 初期化関数を実行して祝日データをセット
initializeHolidays();

