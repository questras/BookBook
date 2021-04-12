package com.example.bookbook.db;

import androidx.lifecycle.LiveData;

import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;
import retrofit2.http.PUT;

public interface SignService {

    @POST("/api/auth/acquire_token")
    @FormUrlEncoded
    LiveData<responseToken> acquireToken(@Field("email") String email,
                                         @Field("password") String password,
                                         @Field("device") String device);

    @POST("/api/auth/revoke_token")
    @FormUrlEncoded
    LiveData<responseToken> revokeToken(@Field("token") String token);

    @PUT("/api/auth/renew_token")
    @FormUrlEncoded
    LiveData<responseToken> renew_Token(@Field("token") String token);

    @POST("/api/auth/register")
    @FormUrlEncoded
    LiveData<responseToken> register(@Field("email") String email,
                                     @Field("password") String password,
                                     @Field("first_name") String firstName,
                                     @Field("last_name") String lastName);
}
