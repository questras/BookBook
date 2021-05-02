package pl.mimuw.bookbook.db.sign;

import android.util.Log;
import android.util.Pair;

import androidx.annotation.NonNull;
import androidx.lifecycle.MutableLiveData;

import pl.mimuw.bookbook.db.ResponseToken;
import pl.mimuw.bookbook.db.RetrofitGson;

import org.json.JSONException;
import org.json.JSONObject;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

/*
 * Class responsible for endpoints interaction with tokens and registration
 */
public class SignRepository {

    private static final String device = "Smartphone";
    private static final String success = "{\"success\":1}";
    private static SignRepository signRepository;
    private final SignService api;

    private SignRepository() {
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

    public void register(String email, String pass, String firstName, String lastName,
                         MutableLiveData<JSONObject> data) {
        api.register(new RequestRegister(email, pass, firstName, lastName)).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(@NonNull Call<Void> call,
                                   @NonNull Response<Void> response) {
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

            @Override
            public void onFailure(@NonNull Call<Void> call, @NonNull Throwable t) {
                Log.d("Response", "Failure");
                data.setValue(null);
            }
        });
    }

}
