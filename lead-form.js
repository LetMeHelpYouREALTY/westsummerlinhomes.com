(function () {
  function showStatus(form, type, message) {
    var status = form.querySelector('.form-status');
    if (!status) {
      status = document.createElement('p');
      status.className = 'form-status';
      form.appendChild(status);
    }

    status.className = 'form-status form-status-' + type;
    status.textContent = message;
    status.hidden = false;
  }

  function initValuationForm() {
    var form = document.getElementById('valuation-form');
    if (!form) {
      return;
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      var submitButton = form.querySelector('button[type="submit"]');
      var formData = new FormData(form);
      var payload = {
        name: String(formData.get('name') || '').trim(),
        phone: String(formData.get('phone') || '').trim(),
        email: String(formData.get('email') || '').trim(),
        address: String(formData.get('address') || '').trim(),
        notes: String(formData.get('notes') || '').trim(),
        type: 'Seller Inquiry',
        source: window.location.href,
      };

      submitButton.disabled = true;
      showStatus(form, 'pending', 'Submitting your valuation request...');

      fetch('/api/leads/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(function (response) {
          return response.json().then(function (data) {
            if (!response.ok) {
              throw new Error(data.error || 'Submission failed');
            }
            return data;
          });
        })
        .then(function () {
          form.reset();
          showStatus(
            form,
            'success',
            'Thank you. Dr. Jan Duffy will follow up with your MLS-based valuation shortly.'
          );
        })
        .catch(function (error) {
          showStatus(
            form,
            'error',
            error.message || 'Unable to submit right now. Please call 702-222-1964.'
          );
        })
        .finally(function () {
          submitButton.disabled = false;
        });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initValuationForm);
  } else {
    initValuationForm();
  }
})();
