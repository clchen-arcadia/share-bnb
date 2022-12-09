import axios from "axios";

const BASE_URL = process.env.REACT_APP_BASE_URL || "http://localhost:5001";

/** API Class.
 *
 * Static class tying together methods used to get/send to to the API.
 * There shouldn't be any frontend-specific stuff here, and there shouldn't
 * be any API-aware stuff elsewhere in the frontend.
 *
 */

class ShareBnbApi {

  static token = localStorage.getItem("token");

  static async request(endpoint, data = {}, method = "get") {
    console.debug("API Call:", endpoint, data, method);

    const url = `${BASE_URL}/${endpoint}`;
    const headers = { token: ShareBnbApi.token };
    const params = (method === "get")
      ? data
      : {};

    try {
      return (await axios({ url, method, data, params, headers })).data;
    } catch (err) {
      console.error("API Error:", err.response);
      let message = err.response.data.error.message;
      throw Array.isArray(message) ? message : [message];
    }
  }

  // Individual API routes
  // TODO: START HERE
  /** Get details on a specific listing */

  static async getListing(handle) {
    let res = await this.request(`companies/${handle}`);
    return res.company;
  }

  /**Get a list of all listings */
  static async getListings() {
    //console.log(this.token);
    let res = await this.request(`companies`);
    return res.companies;
  }

  //  * Register
  //  * user must include { username, password, firstName, lastName, email }
  //  *
  //  * Returns JWT token which can be used to authenticate further requests.
  static async registerNewUser(newUserData) {
    let res = await this.request('/signup', newUserData, 'POST');
    return res.token;
  }

  /** Get token for login from username, password. */

  static async login(data) {
    let res = await this.request(`/login`, data, "post");
    return res.token;
  }

  /** Get the current user. */
  static async getCurrentUser(username) {
    let res = await this.request(`users/${username}`);
    return res.user;
  }

  //TODO:
  //API call to update a users information
  static async updateUserInfo(username, formData) {
    let res = await this.request(`users/${username}`, formData, 'PATCH');
    return res;
  }


}

export default ShareBnbApi;
