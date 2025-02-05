document.addEventListener('DOMContentLoaded', function() {
    const valuationForm = document.getElementById('valuationForm');
    const taxReturnInput = document.getElementById('taxReturn');
    
    if (taxReturnInput) {
        taxReturnInput.addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('tax_return', file);
                
                try {
                    const response = await fetch('/upload_tax_return', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        // Auto-populate form fields with extracted data
                        for (const [key, value] of Object.entries(data)) {
                            const input = document.getElementById(key);
                            if (input) {
                                input.value = value;
                            }
                        }
                    }
                } catch (error) {
                    console.error('Error uploading tax return:', error);
                }
            }
        });
    }
    
    if (valuationForm) {
        valuationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(valuationForm);
            try {
                const response = await fetch('/valuation', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const result = await response.json();
                    displayValuationResult(result);
                }
            } catch (error) {
                console.error('Error submitting valuation:', error);
            }
        });
    }
});

function displayValuationResult(result) {
    const resultDiv = document.getElementById('valuationResult');
    if (resultDiv) {
        document.getElementById('enterpriseValue').textContent = formatCurrency(result.enterprise_value);
        document.getElementById('equityValue').textContent = formatCurrency(result.equity_value);
        document.getElementById('dcfValue').textContent = formatCurrency(result.dcf_value);
        resultDiv.style.display = 'block';
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}
