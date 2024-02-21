// main.js
import { initPage } from './initPage.js'; './initPage.js';
import setupEventListeners from './eventListeners.js'; // イベントリスナーの設定を行う関数をインポート

console.log('mainです。')
// 必要に応じて、他のモジュールや追加の設定をここに記述します。
window.onload = async function() {
    await initPage();
    setupEventListeners();
};