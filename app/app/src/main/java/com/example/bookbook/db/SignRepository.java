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

    public Pair<MutableLiveData<ResponseToken>, JSONObject> authenticate(String email, String pass) {
        MutableLiveData<ResponseToken> token = new MutableLiveData<>();
        final JSONObject[] error = {null};
        api.acquireToken(email, pass, device).enqueue(new Callback<ResponseToken>() {
            @Override
            public void onResponse(@NonNull Call<ResponseToken> call,
                                   @NonNull Response<ResponseToken> response) {
                if (response.isSuccessful()) {
                    token.setValue(response.body());
                } else {
                    token.setValue(null);
                    try {
                        if (response.errorBody() != null)
                            error[0] = new JSONObject(response.errorBody().string());
                    } catch (Exception e) {
                        Log.d("Response", "Exception during response handling");
                    }
                }
            }

            @Override
            public void onFailure(@NonNull Call<ResponseToken> call,
                                  @NonNull Throwable t) {
                token.setValue(null);
            }
        });
        return new Pair<>(token, error[0]);
    }

}
