package hdfs.test;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class CopyFromLocal {
    public static void main( String[] args ) throws Exception
    {
        if(args.length < 2){
            System.out.println("Parameter error");
            return;
        }
        String srcDir = args[0];
        String distDir = args[1];

        FileSystem fs = FileSystem.get(Config.getHdfsConfig());
        fs.copyFromLocalFile(new Path(srcDir),new Path(distDir));
        fs.close();
        System.out.println("Copy local file to HDFS success!");
    }
}
