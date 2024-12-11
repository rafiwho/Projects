document.addEventListener('DOMContentLoaded', function(){

    function fetchLogin(event){
        fetch('/login')
            .then(response => {
                if (response.ok) {
                    window.location.href = '/login'; // Redirect to login.html
                } else {
                    console.error('Failed to fetch login page');
                }
            })
            .catch(error => {
                console.error('Error fetching login page:', error);
            });
    }

    const loginData = document.querySelector('#handleLogin');
    loginData.addEventListener('click', fetchLogin);


    function fetchSignup(event){
        fetch('/signup')
            .then(response => {
                if (response.ok) {
                    window.location.href = '/signup'; // Redirect to login.html
                } else {
                    console.error('Failed to fetch signup page');
                }
            })
            .catch(error => {
                console.error('Error fetching signup page:', error);
            });
    }

    const signupData = document.querySelector('#handleSignup');
    signupData.addEventListener('click',fetchSignup);
});
