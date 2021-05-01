package com.example.bookbook.db.main;

import android.util.Log;

import androidx.annotation.NonNull;
import androidx.lifecycle.MutableLiveData;

import com.example.bookbook.db.RetrofitGson;

import org.json.JSONException;
import org.json.JSONObject;

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
                "Token " + token).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(@NonNull Call<Void> call,
                                   @NonNull Response<Void> response) {
                genericOnResponse(response, data);
            }

            @Override
            public void onFailure(@NonNull Call<Void> call, @NonNull Throwable t) {
                Log.d("Response", "Failure");
                data.setValue(null);
            }
        });
    }

    /*Generic function when we only care whether response was successful
    unless returns error messages*/
    private void genericOnResponse(@NonNull Response<Void> response,
                                   MutableLiveData<JSONObject> data) {
        if (response.isSuccessful()) {
            try {
                data.setValue(new JSONObject(success));
            } catch (JSONException e) {
                Log.d("JSON", "Error during creation");
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
