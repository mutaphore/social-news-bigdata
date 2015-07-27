import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.LongWritable; 
import org.apache.hadoop.io.ArrayWritable; 
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class VoteCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private String getSubreddit(String line) {
        String[] parts = line.split(",");
        if (parts.length != 9) {
            return "";
        }
        return parts[7];
    }

    private int getNumVotes(String line) {
        String[] parts = line.split(",");
        if (parts.length != 9) {
            return 0;
        }
        try {
            return Integer.parseInt(parts[1]);
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    // Map from api info to the post type
    private String getPostType(String line) {
        String[] parts = line.split(",");
        //Types: video, image, article
        String url = parts[3];
        String subreddit = parts[7];
    }

    @Override
    public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        String line = value.toString(); 
        String[] parts = line.split(",");
        // Assumes that after splitting by "," we have following Reddit fields: 
        // id, score, title, url, author, num_comments, created_utc, subreddit, domain
        String subreddit = getSubreddit(line);
        int numVotes = getNumVotes(line);
        if (subreddit.equals("") || numVotes == 0) {
            return;
        }
        context.write(new Text(subreddit), new IntWritable(numVotes));
    }
}