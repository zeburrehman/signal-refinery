document.addEventListener('DOMContentLoaded', () => {
  const fetchFilingsForm = document.getElementById('fetch-filings-form');
  const filings10kList = document.getElementById('filings-10k-list');
  const filings10qList = document.getElementById('filings-10q-list');
  const loadingIndicator = document.getElementById('loading-indicator');
  const summaryResult = document.getElementById('summary-result');

  // Function to display 10-K filings
  function displayFilings10K(filings) {
    filings10kList.innerHTML = '';
    if (filings.length === 0) {
      filings10kList.innerHTML = '<li>No 10-K reports found.</li>';
      return;
    }
    filings.forEach((filing) => {
      const li = document.createElement('li');
      const filingDate = new Date(filing.filing_date).toLocaleDateString();
      const periodDate = filing.period_of_report
        ? new Date(filing.period_of_report).toLocaleDateString()
        : 'N/A';

      li.innerHTML = `
                <div class="filing-item">
                    <div class="filing-info">
                        <strong>Filing Date:</strong> ${filingDate}<br>
                        <strong>Period:</strong> ${periodDate}<br>
                        <strong>Year:</strong> ${filing.year}
                    </div>
                    <a href="${filing.url}" target="_blank" class="filing-link">View on SEC.gov →</a>
                </div>
            `;
      filings10kList.appendChild(li);
    });
  }

  // Function to display 10-Q filings
  function displayFilings10Q(filings) {
    filings10qList.innerHTML = '';
    if (filings.length === 0) {
      filings10qList.innerHTML = '<li>No 10-Q reports found.</li>';
      return;
    }
    filings.forEach((filing) => {
      const li = document.createElement('li');
      const filingDate = new Date(filing.filing_date).toLocaleDateString();
      const periodDate = filing.period_of_report
        ? new Date(filing.period_of_report).toLocaleDateString()
        : 'N/A';

      li.innerHTML = `
                <div class="filing-item">
                    <div class="filing-info">
                        <strong>Filing Date:</strong> ${filingDate}<br>
                        <strong>Period:</strong> ${periodDate}<br>
                        <strong>Quarter:</strong> Q${filing.quarter} ${filing.year}
                    </div>
                    <a href="${filing.url}" target="_blank" class="filing-link">View on SEC.gov →</a>
                </div>
            `;
      filings10qList.appendChild(li);
    });
  }

  // Function to display summary
  function displaySummary(data) {
    summaryResult.innerHTML = `
            <div class="summary-container">
                <h3>Fetch Results for ${data.symbol}</h3>
                <p><strong>Company:</strong> ${data.company_name}</p>
                <div class="summary-stats">
                    <div class="stat">
                        <h4>10-K Reports</h4>
                        <p class="stat-value">${data.total_10k}</p>
                        <p class="stat-label">Added: <span class="stat-added">${data.filings_10k_added}</span></p>
                    </div>
                    <div class="stat">
                        <h4>10-Q Reports</h4>
                        <p class="stat-value">${data.total_10q}</p>
                        <p class="stat-label">Added: <span class="stat-added">${data.filings_10q_added}</span></p>
                    </div>
                </div>
            </div>
        `;
  }

  // Event listener for fetching filings
  fetchFilingsForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const symbol = document.getElementById('fetch-symbol').value.toUpperCase();

    // Show loading indicator
    loadingIndicator.classList.remove('hidden');
    summaryResult.innerHTML = '';
    filings10kList.innerHTML = '';
    filings10qList.innerHTML = '';

    try {
      const response = await fetch(`/filings/${symbol}`, { method: 'POST' });

      if (response.ok) {
        const result = await response.json();
        displaySummary(result);
        displayFilings10K(result.filings_10k);
        displayFilings10Q(result.filings_10q);
      } else {
        const error = await response.json();
        summaryResult.innerHTML = `<div class="error-message">Error: ${error.detail}</div>`;
      }
    } catch (err) {
      summaryResult.innerHTML = `<div class="error-message">Error: ${err.message}</div>`;
    } finally {
      // Hide loading indicator
      loadingIndicator.classList.add('hidden');
      fetchFilingsForm.reset();
    }
  });

  // Event listener for extracting financials
  const extractFinancialsForm = document.getElementById(
    'extract-financials-form'
  );
  if (extractFinancialsForm) {
    extractFinancialsForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const symbol = document
        .getElementById('financial-symbol')
        .value.toUpperCase();
      const loadingIndicator = document.getElementById(
        'financial-loading-indicator'
      );

      loadingIndicator.classList.remove('hidden');

      try {
        const response = await fetch(`/financials/extract/${symbol}`, {
          method: 'POST'
        });

        if (response.ok) {
          const result = await response.json();
          alert(
            `Extracted ${result.metrics_added} financial metrics for ${symbol}. Total: ${result.total_metrics}`
          );
          loadFinancials(symbol);
        } else {
          const error = await response.json();
          alert(`Error: ${error.detail}`);
        }
      } catch (err) {
        alert(`Error: ${err.message}`);
      } finally {
        loadingIndicator.classList.add('hidden');
        extractFinancialsForm.reset();
      }
    });
  }

  // Function to load and display financials
  async function loadFinancials(symbol, statementType = 'income_statement') {
    try {
      const url = statementType
        ? `/financials/${symbol}?statement_type=${statementType}`
        : `/financials/${symbol}`;

      const response = await fetch(url);

      if (response.ok) {
        const data = await response.json();
        displayFinancials(data, statementType);
      }
    } catch (err) {
      console.error('Error loading financials:', err);
    }
  }

  // Function to display financials as table
  function displayFinancials(data, statementType) {
    const display = document.getElementById('financials-display');
    const statement = data.statements[statementType];

    if (!statement || statement.length === 0) {
      display.innerHTML = '<p>No data available for this statement.</p>';
      return;
    }

    // Build table
    let html = '<table class="financial-table"><thead><tr>';
    html +=
      '<th>Metric</th><th>Value (Millions)</th><th>Period</th><th>Filing</th>';
    html += '</tr></thead><tbody>';

    statement.forEach((item) => {
      html += '<tr>';
      html += `<td>${item.metric_label || item.metric_name}</td>`;
      const valueInMillions = (item.value / 1000000).toFixed(2);
      html += `<td>$${valueInMillions}</td>`;
      html += `<td>${new Date(item.period_end).toLocaleDateString()}</td>`;
      html += `<td>${item.filing_type}</td>`;
      html += '</tr>';
    });

    html += '</tbody></table>';
    display.innerHTML = html;
  }

  // Tab switching
  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      document
        .querySelectorAll('.tab-btn')
        .forEach((b) => b.classList.remove('active'));
      e.target.classList.add('active');

      const statement = e.target.dataset.statement;
      const symbol = document
        .getElementById('financial-symbol')
        .value.toUpperCase();

      if (symbol) {
        loadFinancials(symbol, statement);
      }
    });
  });
});
