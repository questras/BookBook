package com.example.bookbook;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;

public class UserProfile extends Fragment {
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_user_profile, container, false);
        ImageButton likeButton = view.findViewById(R.id.like_button);
        ImageButton dislikeButton = view.findViewById(R.id.dislike_button);

        likeButton.setOnClickListener(new View.OnClickListener() {
            private boolean liked = false;
            @Override
            public void onClick(View v) {
                if (liked)
                    likeButton.setImageResource(R.drawable.ic_like);
                else
                    likeButton.setImageResource(R.drawable.ic_liked);
                liked = !liked;
            }
        });

        dislikeButton.setOnClickListener(new View.OnClickListener() {
            private boolean disliked = false;
            @Override
            public void onClick(View v) {
                if (disliked)
                    dislikeButton.setImageResource(R.drawable.ic_dislike);
                else
                    dislikeButton.setImageResource(R.drawable.ic_disliked);
                disliked = !disliked;
            }
        });

        return view;
    }

}