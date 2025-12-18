async function fetchApi(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({
            message: '서버 오류가 발생했습니다.'
        }));
        throw new Error(errorData.message || 'API 요청에 실패했습니다.');
    }
    return response.json();
}

export function fetchUsers() {
    return fetchApi('/api/mngr_sett/users');
}

export function updateUserStatus(userId, status) {
    return fetchApi('/api/mngr_sett/users/status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            user_stat: status
        })
    });
}

export function deleteUser(userId) {
    return fetchApi('/api/mngr_sett/users/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId
        })
    });
}

export function addUser(userId, userName, userPw) {
    return fetchApi('/api/mngr_sett/users/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            user_nm: userName,
            user_pw: userPw
        })
    });
}

export function fetchPermissions() {
    return fetchApi('/api/mngr_sett/permissions');
}

export function updateUserPermissions(userId, permissions) {
    return fetchApi('/api/mngr_sett/users/permissions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            permissions: permissions
        })
    });
}