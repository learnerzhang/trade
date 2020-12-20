import axios from 'axios'
import {
  Message,
  Loading
} from 'element-ui'
// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 50000 // request timeout
})
let loadingInstance = null;
let timeoutHider = null;
function hideLoading() {
  clearTimeout(timeoutHider);
  timeoutHider = setTimeout(() => {
    loadingInstance.close();
  }, 600);
}
// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    loadingInstance = Loading.service({
      fullscreen: true,
      text: "正在拼命加载中...",
      background: "rgba(0, 0, 0, 0.6)"
    });
    config.headers.token = localStorage.getItem('token')

    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    hideLoading();
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data
    hideLoading();
    // if the custom code is not 100, it is judged as an error.
    if (res.code !== 200) {
      Message({
        message: res.msg || 'Error check your token or method',
        type: 'error',
        duration: 2 * 1000
      })
      return Promise.reject(new Error(res.msg || 'Error'))
    } else {
      return res
    }
  },
  error => {
    hideLoading();
    console.log('err' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 2 * 1000
    })
    return Promise.reject(error)
  }
)

export default service.request
