package com.example.bookbook;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.text.Editable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

public class SignUp extends Fragment {

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_sign_up, container, false);
        final TextInputLayout passwordTextInput = view.findViewById(R.id.password_text_input);
        final TextInputEditText passwordEditText = view.findViewById(R.id.password_edit_text);
        final TextInputLayout retypePasswordTextInput = view.findViewById(R.id.retype_password_text_input);
        final TextInputEditText retypePasswordEditText = view.findViewById(R.id.retype_password_edit_text);
        MaterialButton signUpButton = view.findViewById(R.id.sign_up_button);

        passwordEditText.setOnKeyListener((v, i, keyEvent) -> {
            if (isPasswordValid(passwordEditText.getText())) {
                passwordTextInput.setError(null);
            }
            return false;
        });

        retypePasswordEditText.setOnKeyListener((v, i, keyEvent) -> {
            if (isPasswordSame(retypePasswordEditText, passwordEditText)) {
                retypePasswordTextInput.setError(null);
            }
            return false;
        });

        signUpButton.setOnClickListener(v -> {
            if (!isPasswordValid(passwordEditText.getText())) {
                passwordTextInput.setError(getString(R.string.error_password_len));
            } else if (!isPasswordSame(retypePasswordEditText, passwordEditText))  {
                retypePasswordTextInput.setError(getString(R.string.error_password_same));
            } else {
                passwordTextInput.setError(null);
                ((WelcomeActivity) getActivity()).switchToMain();
            }
        });

        return view;
    }

    private boolean isPasswordValid(@Nullable Editable text) {
        return text != null && text.length() >= 8;
    }

    private boolean isPasswordSame(EditText text1, EditText text2) {
        return text1.getText().toString().compareTo(text2.getText().toString()) == 0;
    }
}