import request from '@/utils/request'

function getTransData(page, limit, field, order, keywords, industry) {
  return request({ url: '/tran/daily_trans', method: 'post', params: { page, limit, field, order, keywords, industry }})
}

function getShareTran(code) {
  return request({ url: '/tran/get_tran', method: 'get', params: { code }})
}

export { getShareTran, getTransData }
