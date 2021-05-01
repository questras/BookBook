package com.example.bookbook.db.main;

import com.example.bookbook.db.RequestRegister;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Header;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface MainService {

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/offers/")
    Call<Void> addOffer(@Body RequestAddOffer request, @Header("Authorization") String token);

}
