import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/login/',
    method: 'post',
    data
  })
}

// 注册
export function register(data) {
  return request({
    url: '/register/',
    method: 'post',
    data
  })
}

// 退出登录
export function logout() {
  return request({
    url: '/logout/',
    method: 'post'
  })
}

// 获取用户信息
export function getProfile() {
  return request({
    url: '/profile/',
    method: 'get'
  })
}

// 获取投资类型
export function getInvestmentTypes() {
  return request({
    url: '/investment-types/',
    method: 'get'
  })
}
