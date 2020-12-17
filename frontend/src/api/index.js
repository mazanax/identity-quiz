const API_HOST = process.env.VUE_APP_SITE_HOST || 'http://localhost:5000';

const apiUrl = (path) => {
    return `${API_HOST}${path}`;
}

export const api = {
    makeRequest(method, path, options = null, authorized = true) {
        if (!options) {
            options = {};
        }

        options.method = method;
        options.headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {}),
        }
        if (authorized) {
            options.headers = {...options.headers, 'Authorization': localStorage.getItem('token')};
        }

        return fetch(apiUrl(path), options)
            .then(async (response) => {
                if (!response.ok) {
                    if (response.status === 401) {
                        // localStorage.removeItem('token');

                        if (!options['noReload']) {
                            location.reload();
                        }
                    }

                    return Promise.reject(response);
                }

                return response;
            });
    }
};