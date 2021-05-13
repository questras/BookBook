package pl.mimuw.bookbook.ui;

import android.content.Context;
import android.graphics.Bitmap;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.net.URL;
import java.util.ArrayList;

import pl.mimuw.bookbook.R;
import pl.mimuw.bookbook.db.main.Offer;

public class BrowseAdapter extends RecyclerView.Adapter<BrowseAdapter.ViewHolder> {

    Context context;
    private ArrayList<Offer> offers;

    public BrowseAdapter(Context context, ArrayList<Offer> offers) {
        this.context = context;
        this.offers = offers;
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
//        if (imageUrl != null) {
//            holder.book.setImageBitmap(Bitmap.createScaledBitmap(offerImageToDisplay,
//                    500, 500, true));
//        }
    }

    @Override
    public int getItemCount() {
        return Math.min(offers.size(), 100);
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
}
