document.addEventListener('DOMContentLoaded', () => {
    // ナビゲーションバーのスクロールシャドウ効果
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5)';
        } else {
            navbar.style.boxShadow = 'none';
        }
    });

    // スムーズスクロール
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // メルマガフォーム送信フィードバック
    const form = document.getElementById('newsletter-form');
    const emailInput = document.getElementById('email-input');
    const formMessage = document.getElementById('form-message');

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = emailInput.value.trim();
            if (email) {
                formMessage.className = 'form-message success';
                formMessage.textContent = '🎉 ご登録ありがとうございます！確認メールをお送りしました。';
                emailInput.value = '';
                setTimeout(() => {
                    formMessage.textContent = '';
                }, 5000);
            }
        });
    }
});
