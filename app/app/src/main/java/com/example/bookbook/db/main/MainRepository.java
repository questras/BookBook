package com.example.bookbook.db.main;

import android.util.Log;

import androidx.annotation.NonNull;
import androidx.lifecycle.MutableLiveData;

import com.example.bookbook.db.RetrofitGson;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainRepository {

    private static final String success = "{\"success\":1}";
    private static MainRepository mainRepository;
    private final MainService api;

    private MainRepository() {
        api = RetrofitGson.createService(MainService.class);
    }

    public static MainRepository getInstance() {
        if (mainRepository == null) {
            mainRepository = new MainRepository();
        }
        return mainRepository;
    }

    public void addOffer(String title, String author, String description,
                         String state, String city, String lender_phone,
                         String token, MutableLiveData<JSONObject> data) {
        api.addOffer(new RequestAddOffer(title, author, description, state, city, lender_phone),
                "Token " + token).enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(@NonNull Call<ResponseBody> call,
                                   @NonNull Response<ResponseBody> response) {
                genericOnResponse(response, data);
            }

            @Override
            public void onFailure(@NonNull Call<ResponseBody> call, @NonNull Throwable t) {
                Log.d("Response", "Failure");
                data.setValue(null);
            }
        });
    }

    public void addImage(int id, File imageFile, String token, MutableLiveData<JSONObject> data) {
        RequestBody reqImage = RequestBody.create(MediaType.parse("image/*"), imageFile);
        RequestBody offer = RequestBody.create(MediaType.parse("text/plain"), String.valueOf(id));
        MultipartBody.Part imagePart = MultipartBody.Part.createFormData("image", "image.jpg", reqImage);
        MultipartBody.Part offerPart = MultipartBody.Part.createFormData("offer", null, offer);
        api.addImage("Token " + token, imagePart, offerPart).
                enqueue(new Callback<ResponseBody>() {
                    @Override
                    public void onResponse(@NonNull Call<ResponseBody> call,
                                           @NonNull Response<ResponseBody> response) {
                        genericOnResponse(response, data);
                    }

                    @Override
                    public void onFailure(@NonNull Call<ResponseBody> call, @NonNull Throwable t) {
                        Log.d("Response", "Failure");
                        data.setValue(null);
                    }
                });
    }

    public void signOut(String token, MutableLiveData<JSONObject> data) {
        api.revokeToken(new RequestRevokeToken(token)).enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(@NonNull Call<ResponseBody> call,
                                   @NonNull Response<ResponseBody> response) {
                genericOnResponse(response, data);
            }

            @Override
            public void onFailure(@NonNull Call<ResponseBody> call, @NonNull Throwable t) {
                Log.d("Response", "Failure");
                data.setValue(null);
            }
        });
    }

    /*Generic function for handling responses and converting to JSONObjects*/
    private void genericOnResponse(@NonNull Response<ResponseBody> response,
                                   MutableLiveData<JSONObject> data) {
        if (response.isSuccessful()) {
            try {
                if (response.body() == null) {
                    data.setValue(new JSONObject(success));
                } else {
                    JSONObject res = new JSONObject(response.body().string());
                    data.setValue(res);
                }
            } catch (JSONException e) {
                Log.d("JSON", "Error during creation");
            } catch (IOException e) {
                Log.d("JSON", "Error during response conversion");
            }
        } else {
            try {
                if (response.errorBody() != null) {
                    data.setValue(new JSONObject(response.errorBody().string()));
                }
            } catch (Exception e) {
                Log.d("Response error", "Exception during response handling");
            }
        }
    }

}
