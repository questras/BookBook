package com.example.bookbook.db.main;

import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Field;
import retrofit2.http.Header;
import retrofit2.http.Headers;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface MainService {

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/offers/")
    Call<ResponseBody> addOffer(@Body RequestAddOffer request, @Header("Authorization") String token);

    @Multipart
    @POST("api/offer_images/")
    Call<ResponseBody> addImage(@Header("Authorization") String token,
                                @Part MultipartBody.Part imagePart,
                                @Part MultipartBody.Part offerPart);

    @Headers({"Accept: application/json", "Content-Type: application/json"})
    @POST("api/auth/revoke_token")
    Call<ResponseBody> revokeToken(@Body RequestRevokeToken request);

}
