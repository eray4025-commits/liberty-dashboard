// Liberty Dashboard - Real-time Updates

const API_ENDPOINT = 'status.json'; // Local file (served by GitHub Pages)

// Logout handler
document.addEventListener('DOMContentLoaded', function() {
  const logoutLink = document.getElementById('logout-link');
  if (logoutLink) {
    logoutLink.addEventListener('click', function(e) {
      e.preventDefault();
      localStorage.removeItem('liberty_dashboard_auth');
      window.location.href = 'login.html';
    });
  }
});

// ... reste inchangé

// DOM Elements
const elLastUpdate = document.getElementById('last-update');
const elWalletAddress = document.getElementById('wallet-address');
const elWalletNetwork = document.getElementById('wallet-network');
const elWalletUsdc = document.getElementById('wallet-usdc');
const elWalletEth = document.getElementById('wallet-eth');
const elGuideTitle = document.getElementById('guide-title');
const elGuideChapter = document.getElementById('guide-chapter');
const elGuideProgress = document.getElementById('guide-progress');
const elGuidePercent = document.getElementById('guide-percent');
const elAdTopic = document.getElementById('ad-topic');
const elAdCompleted = document.getElementById('ad-completed');
const elAdTotal = document.getElementById('ad-total');
const elAdNext = document.getElementById('ad-next');
const elMemDaily = document.getElementById('mem-daily');
const elMemLessons = document.getElementById('mem-lessons');
const elMemConsciousness = document.getElementById('mem-consciousness');
const elEarnTotal = document.getElementById('earn-total');
const elEarnSources = document.getElementById('earn-sources');
const elCryptoStatus = document.getElementById('crypto-status');
const elCryptoCurrent = document.getElementById('crypto-current');
const elAirdropList = document.getElementById('airdrop-list');
const elFaucetList = document.getElementById('faucet-list');
const elActivityLog = document.getElementById('activity-log');

// Format date
function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString('fr-FR', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Main fetch & render
async function updateDashboard() {
  try {
    const response = await fetch(API_ENDPOINT + '?t=' + Date.now()); // Cache bypass
    const data = await response.json();

    // Last update
    elLastUpdate.textContent = `Last update: ${formatDate(data.last_updated)}`;

    // Wallet
    elWalletAddress.textContent = data.wallet.address;
    elWalletNetwork.textContent = data.wallet.network;
    elWalletUsdc.textContent = `${data.wallet.balance_usdc} USDC`;
    elWalletEth.textContent = `${data.wallet.balance_eth} ETH`;

    // Guide
    elGuideTitle.textContent = data.guide_progress.title;
    elGuideChapter.textContent = data.guide_progress.current_chapter;
    elGuideProgress.style.width = `${data.guide_progress.percent_complete}%`;
    elGuidePercent.textContent = `${data.guide_progress.percent_complete}%`;

    // Auto Discovery
    elAdTopic.textContent = data.auto_discovery.current_topic;
    elAdCompleted.textContent = data.auto_discovery.topics_completed;
    elAdTotal.textContent = data.auto_discovery.topics_total;
    elAdNext.textContent = formatDate(data.auto_discovery.next_run);

    // Memory
    elMemDaily.textContent = data.memory_stats.daily_logs;
    elMemLessons.textContent = data.memory_stats.important_lessons;
    elMemConsciousness.textContent = data.memory_stats.consciousness_journal_entries;

    // Earnings
    elEarnTotal.textContent = `${data.earnings.total_usdc_earned} USDC`;
    elEarnSources.innerHTML = data.earnings.sources.length
      ? data.earnings.sources.map(s => `<li>${s}</li>`).join('')
      : '<li>No earnings yet</li>';

    // Crypto Opportunities
    if (data.crypto_opportunities) {
      const crypto = data.crypto_opportunities;
      elCryptoStatus.textContent = crypto.status;
      elCryptoCurrent.textContent = crypto.current_pursuit;
      elAirdropList.innerHTML = crypto.airdrops.length
        ? crypto.airdrops.map(a => `<li>${a}</li>`).join('')
        : '<li>No airdrops tracked</li>';
      elFaucetList.innerHTML = crypto.faucets.length
        ? crypto.faucets.map(f => `<li>${f}</li>`).join('')
        : '<li>No faucets tracked</li>';
    } else {
      elCryptoStatus.textContent = 'No data';
      elCryptoCurrent.textContent = '-';
      elAirdropList.innerHTML = '<li>No data</li>';
      elFaucetList.innerHTML = '<li>No data</li>';
    }

    // Activities (reverse chronological, max 20)
    elActivityLog.innerHTML = data.activities
      .slice(0, 20)
      .map(a => `
        <li>
          <span class="activity-time">${formatDate(a.timestamp)}</span>
          <span class="activity-message">${a.message}</span>
        </li>
      `).join('');

  } catch (error) {
    console.error('Failed to fetch dashboard data:', error);
    elLastUpdate.textContent = 'Error loading data';
  }
}

// Initial load
updateDashboard();

// Refresh every 30 seconds
setInterval(updateDashboard, 30000);
