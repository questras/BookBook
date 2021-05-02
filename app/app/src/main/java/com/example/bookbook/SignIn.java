package com.example.bookbook;

import android.os.Bundle;
import android.text.Editable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.bookbook.db.SignViewModel;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import org.json.JSONObject;

public class SignIn extends Fragment {

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_sign_in, container, false);
        final TextInputLayout passwordTextInput = view.findViewById(R.id.password_text_input);
        final TextInputEditText passwordEditText = view.findViewById(R.id.password_edit_text);
        final TextInputLayout mailTextInput = view.findViewById(R.id.mail_text_input);
        final TextInputEditText mailEditText = view.findViewById(R.id.mail_edit_text);
        MaterialButton signUpButton = view.findViewById(R.id.add_offer_button);
        MaterialButton signInButton = view.findViewById(R.id.sign_in_button);

        SignViewModel model = new ViewModelProvider(requireActivity()).get(SignViewModel.class);
        model.getToken().observe(requireActivity(), response -> {
//            Wrong credentials handling
            if (response != null && response.first == null) {
                JSONObject err = response.second;

                if (err.has("email"))
                    mailTextInput.setError(err.optJSONArray("email").optString(0));
                else
                    mailTextInput.setError(null);

                if (err.has("password"))
                    passwordTextInput.setError(err.optJSONArray("password").optString(0));
                else if (err.has("non_field_errors"))
                    passwordTextInput.setError("Wrong password or mail");
                else
                    passwordTextInput.setError(null);
            }
        });

        mailEditText.setOnKeyListener((v, i, keyEvent) -> {
            if (isMailValid(mailEditText.getText())) {
                mailTextInput.setError(null);
            }
            return false;
        });

        passwordEditText.setOnKeyListener((v, i, keyEvent) -> {
            if (isPasswordValid(passwordEditText.getText())) {
                passwordTextInput.setError(null);
            }
            return false;
        });

        signInButton.setOnClickListener(v -> {
            model.authenticate(mailEditText.getText().toString(), passwordEditText.getText().toString());
        });

        signUpButton.setOnClickListener(v -> {
            mailTextInput.setError(null);
            passwordTextInput.setError(null);
            ((NavigationHost) requireActivity()).navigateTo(new SignUp(), true);
        });

        return view;
    }

    private boolean isPasswordValid(@Nullable Editable text) {
        return text != null && text.length() >= 8;
    }

    private boolean isMailValid(@Nullable Editable text) {
        return text != null && text.toString().contains("@");
    }
}