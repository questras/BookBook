package com.example.bookbook.db;

import android.util.Log;
import android.util.Pair;

import androidx.annotation.NonNull;
import androidx.lifecycle.MutableLiveData;

import org.json.JSONObject;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SignRepository {

    private static final String device = "Smartphone";
    private static SignRepository signRepository;
    private final SignService api;

    public SignRepository() {
        api = RetrofitGson.createService(SignService.class);
    }

    public static SignRepository getInstance() {
        if (signRepository == null) {
            signRepository = new SignRepository();
        }
        return signRepository;
    }

    public void authenticate(String email, String pass,
                             MutableLiveData<Pair<ResponseToken, JSONObject>> data) {
        api.acquireToken(new RequestToken(email, pass, device)).enqueue(new Callback<ResponseToken>() {
            @Override
            public void onResponse(@NonNull Call<ResponseToken> call,
                                   @NonNull Response<ResponseToken> response) {
                if (response.isSuccessful()) {
                    data.setValue(new Pair<>(response.body(), null));
                } else {
                    try {
                        if (response.errorBody() != null) {
                            data.setValue(new Pair<>(null, new JSONObject(response.errorBody().string())));
                        }
                    } catch (Exception e) {
                        Log.d("Response", "Exception during response handling");
                    }
                }
            }

            @Override
            public void onFailure(@NonNull Call<ResponseToken> call,
                                  @NonNull Throwable t) {
                Log.d("Response", "Failure");
                data.setValue(null);
            }
        });
    }

}
