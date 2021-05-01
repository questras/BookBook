package com.example.bookbook.db.main;

import com.example.bookbook.db.RequestRegister;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Header;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface MainService {

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/offers/")
    Call<ResponseBody> addOffer(@Body RequestAddOffer request, @Header("Authorization") String token);

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/offer_images/")
    Call<ResponseBody> addImage(@Body RequestImage request, @Header("Authorization") String token);

}
