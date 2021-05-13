package pl.mimuw.bookbook.ui;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;

import pl.mimuw.bookbook.R;
import pl.mimuw.bookbook.db.main.Offer;

import static java.util.concurrent.Executors.newCachedThreadPool;

public class BrowseAdapter extends RecyclerView.Adapter<BrowseAdapter.ViewHolder> {

    private Context context;
    private ArrayList<Offer> offers;
    private ExecutorService threadPool;

    public BrowseAdapter(Context context, ArrayList<Offer> offers) {
        this.context = context;
        this.offers = offers;
        threadPool = newCachedThreadPool();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).
                inflate(R.layout.offer_view, parent, false);

        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.title.setText(offers.get(position).getTitle());
        holder.author.setText(offers.get(position).getAuthor());
        URL imageUrl = offers.get(position).getImageUrl();
        if (imageUrl != null) {
            threadPool.execute(new SetImage(holder.book, imageUrl));
        }
    }

    @Override
    public int getItemCount() {
        return Math.min(offers.size(), 200);
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        private TextView title;
        private TextView author;
        private ImageView book;

        public ViewHolder(@NonNull View view) {
            super(view);
            book = view.findViewById(R.id.book_image);
            author = view.findViewById(R.id.author);
            title = view.findViewById(R.id.title);

            view.setOnClickListener(v -> {
                Toast.makeText(context, "Hello!", Toast.LENGTH_SHORT).show();
            });
        }
    }

    private class SetImage implements Runnable {
        private final ImageView toSet;
        private final URL imageUrl;

        public SetImage(ImageView toSet, URL imageUrl) {
            this.toSet = toSet;
            this.imageUrl = imageUrl;
        }

        @Override
        public void run() {
            try {
                Bitmap image = BitmapFactory.decodeStream(imageUrl.openConnection().getInputStream());
                ((Activity) context).runOnUiThread(() -> {
                    toSet.setImageBitmap(Bitmap.createScaledBitmap(image, 500, 500, true));
                });
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
