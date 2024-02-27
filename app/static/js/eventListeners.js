// eventListeners.js
import { setFormReadOnly, updateFormData, updateFinancials } from './formUtils.js';
import { fetchHolidays } from './holidays.js';
import { handleDateChange } from './dateHandlers.js';
export default async function setupEventListeners() {
    // 祝日データをフェッチして、グローバル変数または状態管理に保存
    let holidays = {};
    try {
        holidays = await fetchHolidays();
    } catch (error) {
        console.error('Failed to fetch holidays:', error);
        // エラーハンドリング: ユーザーへの通知、デフォルト値の設定など
    }

    // 日付フィールドに対するイベントリスナー
    document.getElementById('date').addEventListener('change', handleDateChange)
    document.getElementById('card_total').addEventListener('input', updateFinancials);
    document.getElementById('usd_total').addEventListener('input', updateFinancials);
    document.getElementById('customers').addEventListener('input', updateFinancials);
    document.getElementById('cash_total').addEventListener('input', updateFinancials);


    // フォーム送信時のイベントリスナー
    document.querySelector('form').addEventListener('submit', async function (e) {
        e.preventDefault(); // デフォルトのフォーム送信を防止
        await updateFinancials(); // お金関連データの最終更新
        // ここで、フォームデータの送信やその他の送信前処理を行う
        e.target.submit()
    });
}
// ページロード時にイベントリスナーをセットアップ
document.addEventListener('DOMContentLoaded', setupEventListeners);