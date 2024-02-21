import { fetchHolidays, calculateLastBusinessDay } from './holidays.js';
import { setFormReadOnly, clearFormData, updateFinancials } from './formUtils.js';
import { logError, logInfo } from './logging.js';

async function initializePage() {
    try {
        const holidays = await fetchHolidays();
        const businessDay = calculateLastBusinessDay(holidays);
        document.getElementById('date').value = businessDay;
        // ここでビジネスデーをサーバーに送信するロジックを追加
        // サーバーからの応答に基づいてフォームの状態を更新
    } catch (error) {
        logError('Error initializing page', error);
        alert('ページの初期化中にエラーが発生しました。');
    }
}

function setupEventHandlers() {
    document.getElementById('date').addEventListener('change', async function() {
        try {
            const selectedDate = this.value;
            // 日付に基づいてフォームの状態を更新するロジックを追加
            logInfo(`Selected date changed to ${selectedDate}`);
        } catch (error) {
            logError('Error handling date change', error);
            alert('日付の変更時にエラーが発生しました。');
        }
    });

    // 他のイベントハンドラーをここに追加
    document.querySelector('form').addEventListener('submit', function(event) {
        updateFinancials();
        // 必要に応じてe.preventDefault()を使用してデフォルトのフォーム送信を防止
    });
}

window.onload = async function() {
    await initializePage();
    setupEventHandlers();
};
