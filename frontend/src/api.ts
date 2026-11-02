import axios from 'axios';
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://localhost:8000/api/v1',timeout:60000});
api.interceptors.request.use(c=>{const t=localStorage.getItem('rp_access');if(t)c.headers.Authorization=`Bearer ${t}`;return c;});
api.interceptors.response.use(r=>r,e=>{if(e.response?.status===401){localStorage.removeItem('rp_access');localStorage.removeItem('rp_refresh');}return Promise.reject(e);});
export const message=(e:unknown)=>{if(axios.isAxiosError(e))return e.response?.data?.detail||e.message;return 'Something went wrong. Please try again.'};
