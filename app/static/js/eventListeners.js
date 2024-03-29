// eventListeners.js
import { setFormReadOnly, updateFormData, updateFinancials } from './formUtils.js';
import { fetchHolidays } from './holidays.js';
import { handleDateChange } from './dateHandlers.js';
import { showBootstrapAlert } from './dateHandlers.js';
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
    // 既存のイベントリスナー設定に追加
    document.getElementById('rakuten_pay').addEventListener('input', updateFinancials);
    document.getElementById('paypay').addEventListener('input', updateFinancials);


    // フォーム送信時のイベントリスナー
    document.querySelector('form').addEventListener('submit', async function (e) {
        e.preventDefault(); // デフォルトのフォーム送信を防止
        await updateFinancials(); // お金関連データの最終更新
        e.target.submit();


    });
}
// ページロード時にイベントリスナーをセットアップ
// document.addEventListener('DOMContentLoaded', setupEventListeners);

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    // 合計値段フィールドのみを読み取り専用に設定
    document.getElementById('total_price').readOnly = true;
});