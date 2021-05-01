package com.example.bookbook.db;

import retrofit2.Call;
import retrofit2.Response;
import retrofit2.http.Body;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.Headers;
import retrofit2.http.POST;
import retrofit2.http.PUT;

/*
 * REST service
 */
public interface SignService {

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/auth/acquire_token")
    Call<ResponseToken> acquireToken(@Body RequestToken request);

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/auth/register")
    Call<Void> register(@Body RequestRegister request);

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/auth/revoke_token")
    Call<Void> revokeToken(@Field("token") String token);

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @PUT("api/auth/renew_token")
    Call<Void> renew_Token(@Field("token") String token);
}
