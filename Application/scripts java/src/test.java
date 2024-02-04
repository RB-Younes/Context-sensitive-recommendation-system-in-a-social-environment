import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.RoundRectangle2D;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JProgressBar;  
public class test extends JFrame
{
	public static void main(String args[]) {
		 JFrame f = new JFrame("Stepping Progress");
		    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		    
		    f.setUndecorated(true);	
		    f.setResizable(false);
		    f.setSize(600, 200);
		    f.setShape(new RoundRectangle2D.Double(0d, 0d, 600, 200, 25d, 25d));
		    
		    f.setLocationRelativeTo(null);
		    
		    
		    final JProgressBar aJProgressBar = new JProgressBar();
		    aJProgressBar.setBounds(100,92,400, 16);;
		    aJProgressBar.setIndeterminate(true);
		    f.add(aJProgressBar);
		JButton btnStop = new JButton("Stop");
        btnStop.setEnabled(false);
        btnStop.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
			}
		});
        btnStop.setToolTipText("Stop processing");
        btnStop.setBounds(250, 130, 100, 30);
		f.add(btnStop);
		
		JLabel BG = new JLabel("");
		BG.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/process.png")));
		BG.setBounds(0, 0, 600, 200);
		f.add(BG);

	    f.setVisible(true);  
	  }
}