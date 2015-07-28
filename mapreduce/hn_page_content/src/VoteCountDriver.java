import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class VoteCountDriver {

    public static void main(String[] args) throws Exception{

        if (args.length != 2) {
            System.err.println("Usage: VoteCountDriver <input path> <output path> <links|images|scripts|styles>");
            System.exit(-1);
        }

        Job job = new Job();

        job.setJarByClass(VoteCountDriver.class);
        job.setJobName("VoteCount");

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(VoteCountMapper.class);
        job.setReducerClass(VoteCountReducer.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(FloatWritable.class);
        
        job.setOutputFormatClass(CsvOutputFormat.class);

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

}