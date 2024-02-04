import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.awt.geom.RoundRectangle2D;
import java.io.IOException;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JRadioButton;
import javax.swing.JTextField;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import com.formdev.flatlaf.FlatDarculaLaf;



////////////////////////////////////////////////////////////////////////////////-----------Fenetre DATASET------------///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

public class Datasets extends JFrame {
	

	private static final long serialVersionUID = 1L;

	
	private int posX = 0;   //Position X de la souris au clic
    private int posY = 0;   //Position Y de la souris au clic
    

	private JPanel contentPane;
	private JTextField textFieldNONI;
	private JTextField textFieldPath;
	
	private JButton btn1;
	private JButton btn3;
	private JRadioButton RadiobtnYelp;
	private JRadioButton RadiobtnFilmTrust;
	private JRadioButton RadiobtnMovieLens1M;
	private JFileChooser fileChooser;
	private String Folder_Selected;
	private int i=0;
	private String path_open;
	private int p=0;
	private int dataset=0; 
	private boolean DataProcessed = false;

	/**
	 * Launch the application.
	 * @throws UnsupportedLookAndFeelException 
	 */
	public static void main(String[] args) throws UnsupportedLookAndFeelException , IOException, InterruptedException  {
		FlatDarculaLaf.install();	
		UIManager.setLookAndFeel(new FlatDarculaLaf() );
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Datasets frame = new Datasets("-1","NONE",false);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	

	/**
	 * Create the frame.
	 */
	public Datasets(String dataset_,String path_data,Boolean DataProcessed_ ) {
		setIconImage(Toolkit.getDefaultToolkit().getImage(Datasets.class.getResource("/Menu_img/data.png")));
		//cnx

		setUndecorated(true);	
		setResizable(false);

		setTitle("Datasets");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(0, 0, 1100, 650);
		setShape(new RoundRectangle2D.Double(0d, 0d, 1100d, 650d, 25d, 25d));
		setLocationRelativeTo(null);
		//vu que la frame est Undecorated on a besoin de ces MouseListeners pour la faire bouger(frame)
		  addMouseListener(new MouseAdapter() {
	            @Override
	            //on recupere les coordonnées de la souris
	            public void mousePressed(MouseEvent e) {
	                posX = e.getX();    //Position X de la souris au clic
	                posY = e.getY();    //Position Y de la souris au clic
	            }
	        });
	        addMouseMotionListener(new MouseMotionAdapter() {
	            // A chaque deplacement on recalcul le positionnement de la fenetre
	            @Override
	            public void mouseDragged(MouseEvent e) {
	                int depX = e.getX() - posX;
	                int depY = e.getY() - posY;
	                setLocation(getX()+depX, getY()+depY);
	            }
	        });
	        
	        
		contentPane = new JPanel();
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel BGDatasets = new JLabel("");
		BGDatasets.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/1.png")));
		//BGDatasets.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/1.png")));	// Back ground de base	
       
// Bouton Reduire ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton Minimise_BTN = new JButton("");
		Minimise_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Datasets.class.getResource("/Menu_img/Minimize ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Datasets.class.getResource("/Menu_img/Minimize ML .png")));
			}
		});
		Minimise_BTN.setToolTipText("Minimize");
		ButtonStyle(Minimise_BTN);
		Minimise_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setState(ICONIFIED);
				
			}
		});
		Minimise_BTN.setIcon(new ImageIcon(Datasets.class.getResource("/Menu_img/Minimize ML .png")));
		Minimise_BTN.setBounds(932, 11, 32, 32);
		contentPane.add(Minimise_BTN);
//Boutton home//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				JButton btnHome = new JButton("");
				btnHome.addMouseListener(new MouseAdapter() {
					@Override
					public void mouseEntered(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(Datasets.class.getResource("/Models_img/home selected.png")));//changer les couleurs button
						}
					}
					@Override
					public void mouseExited(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(Datasets.class.getResource("/Models_img/home.png")));//remetre le bouton de base
						}
					}
				});
				btnHome.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						if (DataProcessed_==true) {
							Menu frame = new Menu(dataset_,path_data,DataProcessed_);
							frame.setLocationRelativeTo(contentPane);
							frame.setVisible(true);
							dispose();
						}
						else {
							String Path_save =textFieldPath.getText();
							Menu frame = new Menu(String.valueOf(dataset),Path_save,DataProcessed);// retourner au menu medecin
							frame.setLocationRelativeTo(null);
							frame.setVisible(true);
							dispose();
						}
						
					}
				});
				btnHome.setIcon(new ImageIcon(Datasets.class.getResource("/Models_img/home.png")));
				btnHome.setToolTipText("Menu");
				btnHome.setBounds(974, 11, 32, 32);
				ButtonStyle(btnHome);
				contentPane.add(btnHome);
// Exit bouton//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		JButton Exit_BTN = new JButton("");
		Exit_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Datasets.class.getResource("/Menu_img/Exit ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Datasets.class.getResource("/Menu_img/Exit ML.png")));
			}
		});
		Exit_BTN.setToolTipText("Exit");
		ButtonStyle(Exit_BTN);
		Exit_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			
					
					int ClickedButton	=JOptionPane.showConfirmDialog(null, "Do you really want to leave?", "Close", JOptionPane.YES_NO_OPTION);
					if(ClickedButton==JOptionPane.YES_OPTION)
					{					
						dispose();
					}
					
					
			}
			
		});
		Exit_BTN.setIcon(new ImageIcon(Datasets.class.getResource("/Menu_img/Exit ML.png")));
		Exit_BTN.setBounds(1016, 11, 32, 32);
		contentPane.add(Exit_BTN);
//btns ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		btn1= new JButton("");
		btn1.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
					BGDatasets.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/2.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				BGDatasets.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/1.png")));
			}
			
		});
		btn1.setToolTipText("Proceed data");
		btn1.setForeground(Color.WHITE);
		btn1.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
		btn1.addActionListener(new ActionListener() {
			Process process;
			Boolean stopped = false;
			public void actionPerformed(ActionEvent arg0) {
				
		        JFrame f = new JFrame("Stepping Progress");
			    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			    
			    f.setUndecorated(true);	
			    f.setResizable(false);
			    f.setSize(600, 200);
			    f.setShape(new RoundRectangle2D.Double(0d, 0d, 600, 200, 25d, 25d));
			    
			    f.setLocationRelativeTo(null);
			    
			    
			    final JProgressBar aJProgressBar = new JProgressBar();
			    aJProgressBar.setBounds(110,92,400, 16);;
			    aJProgressBar.setIndeterminate(true);
			    f.getContentPane().add(aJProgressBar);
			 

				
				final CyclicBarrier gate = new CyclicBarrier(3);
				Thread t1 = new Thread(){
				    public void run(){
				        try {
							gate.await();
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						} catch (BrokenBarrierException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
				        //do stuff  
				        i=1;
		                DataProcessed=true;
		                dataset =0;
		                if (RadiobtnYelp.isSelected()) dataset=2;
		                
		                if (RadiobtnMovieLens1M.isSelected())  dataset=1;
		                
		                if (RadiobtnFilmTrust.isSelected())  dataset=3;
		                String Str_dataset=String.valueOf(dataset);
		                
		                String Path_save =textFieldPath.getText();
		                
		                String NONI =textFieldNONI.getText();
		                if (!Path_save.equals("C:/Users/name/Desktop/...")) {
		                     Path_save =textFieldPath.getText()+'\\';
		                     path_open=Path_save;
		                     p=1;
		                }
		                 
		                
		                String path_script ="";
		                path_script = Datasets.class.getResource("/scripts_py/DataProcess.py").getPath(); // get the path of the script (a revoir)
		                path_script = path_script.substring(1, path_script.length());
		                ProcessBuilder pb = null;
		                
		                if (!NONI.equals("exp : 1 , 2 ...n") && !Path_save.equals("C:/Users/name/Desktop/...") && dataset!=0) {//CHECK
		                     pb = new ProcessBuilder("python",path_script,"--dataset", Str_dataset,"--negs", NONI ,"--path_save",Path_save).inheritIO();
		                }
		                if (NONI.equals("exp : 1 , 2 ...n") && Path_save.equals("C:/Users/name/Desktop/...") && dataset==0) {//execution par default //CHECK
		                     pb = new ProcessBuilder("python",path_script).inheritIO();
		                }
		                if (!NONI.equals("exp : 1 , 2 ...n") && Path_save.equals("C:/Users/name/Desktop/...") && dataset==0) {//CHECK
		                     pb = new ProcessBuilder("python",path_script,"--negs", NONI).inheritIO();
		                }
		                        
		                if (NONI.equals("exp : 1 , 2 ...n") && !Path_save.equals("C:/Users/name/Desktop/...") && dataset==0) {//CHECK
		                    pb = new ProcessBuilder("python",path_script,"--path_save",Path_save).inheritIO();
		                }
		                
		                if (NONI.equals("exp : 1 , 2 ...n") && Path_save.equals("C:/Users/name/Desktop/...") && dataset!=0) {//CHECK
		                        pb = new ProcessBuilder("python",path_script,"--dataset", Str_dataset).inheritIO();
		                }
		                if (!NONI.equals("exp : 1 , 2 ...n") && !Path_save.equals("C:/Users/name/Desktop/...") && dataset==0) {//CHECK
		                        pb = new ProcessBuilder("python",path_script,"--path_save",Path_save,"--negs", NONI ).inheritIO();
		                }
		                if (!NONI.equals("exp : 1 , 2 ...n") && Path_save.equals("C:/Users/name/Desktop/...") && dataset!=0) {//CHECK
		                         pb = new ProcessBuilder("python",path_script,"--negs", NONI,"--dataset", Str_dataset ).inheritIO();
		                }
		                if (NONI.equals("exp : 1 , 2 ...n") && !Path_save.equals("C:/Users/name/Desktop/...") && dataset!=0) {//CHECK
		                        pb = new ProcessBuilder("python",path_script,"--path_save",Path_save,"--dataset", Str_dataset ).inheritIO();
		                }
		                
		                try {
		                    
		                    process=pb.start();
		                    try {
		                         process.waitFor();
		                    } catch (InterruptedException e1) {
		                        // TODO Auto-generated catch block
		                        e1.printStackTrace();
		                    }
		                    if(!stopped) {
		                    	f.dispose();
							JOptionPane.showMessageDialog(null,  "Data loaded and processed !","state" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/stamp.png")));	
		                    }
		                    else {
		                    	f.dispose();
							JOptionPane.showMessageDialog(null,  "Stopped treatment.","state" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/error.png")));	
							i=0;
			                DataProcessed=false;
			                stopped=false;
							}
							
		                } catch (IOException e) {
		                    // TODO Auto-generated catch block
		                    JOptionPane.showMessageDialog(null,e);
		                }
				    }};
				Thread t2 = new Thread(){
				    public void run(){
				        try {
							gate.await();
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						} catch (BrokenBarrierException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
				        
				        JButton btnStop = new JButton("Stop");
				        btnStop.addMouseListener(new MouseAdapter() {
							@Override
							public void mouseClicked(MouseEvent e) {
								stopped=true;
								process.destroy();
							}
						});
				        btnStop.setToolTipText("Stop processing");
				        btnStop.setBounds(250, 130, 100, 25);
						f.getContentPane().add(btnStop);
						
						JLabel BG = new JLabel("");
						BG.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/process.png")));
						BG.setBounds(0, 0, 600, 200);
						f.getContentPane().add(BG);

					    f.setVisible(true);  
				    }};

				t1.start();
				t2.start();

				// At this point, t1 and t2 are blocking on the gate. 
				// Since we gave "3" as the argument, gate is not opened yet.
				// Now if we block on the gate from the main thread, it will open
				// and all threads will start to do stuff!

				try {
					gate.await();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (BrokenBarrierException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}
		});
		btn1.setBounds(376, 480, 185, 44);
		ButtonStyle(btn1);
		contentPane.add(btn1);
		
		btn3= new JButton("");
		btn3.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
					BGDatasets.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/3.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				BGDatasets.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/1.png")));
			}
		});
		btn3.setToolTipText("Show data");
		btn3.setForeground(Color.WHITE);
		btn3.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
		btn3.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String FolderName="C:/users/"+System.getProperty("user.name")+"/Desktop/";
				if (i==1) {
					if (p==1) {
						p=0;
						FolderName=path_open;
					}
					
					try {
						Runtime.getRuntime().exec("rundll32 url.dll,FileProtocolHandler " + FolderName);
					} catch (IOException ex) {
			             Logger.getLogger(Datasets.class.getName()).log(Level.SEVERE, null, ex);
					}
					
				}
				else {
					JOptionPane.showMessageDialog(null,  "Please process a dataset !","Warning" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/error.png")));	
				}
				
			}
		});
		btn3.setBounds(700, 480, 185, 44);
		ButtonStyle(btn3);
		contentPane.add(btn3);
//radio btns//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
		RadiobtnYelp = new JRadioButton("");
		RadiobtnYelp.setToolTipText("Yelp");
		RadiobtnYelp.setBounds(113, 215, 21, 23);
		contentPane.add(RadiobtnYelp);
		
		RadiobtnFilmTrust = new JRadioButton("");
		RadiobtnFilmTrust.setToolTipText("Film Trust");
		RadiobtnFilmTrust.setBounds(113, 316, 21, 23);
		contentPane.add(RadiobtnFilmTrust);
		
		RadiobtnMovieLens1M = new JRadioButton("");
		RadiobtnMovieLens1M.setToolTipText("Movie Lens (1M)");
		RadiobtnMovieLens1M.setBounds(113, 413, 21, 23);
		contentPane.add(RadiobtnMovieLens1M);
		
		   //Group the radio buttons.
		ButtonGroup group = new ButtonGroup();
		group.add(RadiobtnYelp);
		group.add(RadiobtnFilmTrust);
		group.add(RadiobtnMovieLens1M);
// text fields//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		textFieldNONI = new JTextField();
		
		textFieldNONI.setToolTipText("Number of negative instances");
		textFieldNONI.setBounds(527, 308, 129, 34);
		textFieldNONI.setText("exp : 1 , 2 ...n");
		textFieldNONI.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
		textFieldNONI.setForeground(Color.GRAY);
		textFieldNONI.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		textFieldNONI.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldNONI.getText().toString().equals("exp : 1 , 2 ...n")) {
					textFieldNONI.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldNONI.setForeground(Color.LIGHT_GRAY);
					textFieldNONI.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldNONI.getText().toString().equals("")) {
					textFieldNONI.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldNONI.setForeground(Color.GRAY);
					textFieldNONI.setText("exp : 1 , 2 ...n");
				}
			}
		});
		contentPane.add(textFieldNONI);
		textFieldNONI.setColumns(10);
		
		textFieldPath = new JTextField();
		textFieldPath.setEditable(false);
		textFieldPath.setToolTipText("Path to save train & test files");
		textFieldPath.setText("C:/Users/name/Desktop/...");
		textFieldPath.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
		textFieldPath.setForeground(Color.GRAY);
		textFieldPath.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldPath.getText().toString().equals("C:/Users/name/Desktop/...") && textFieldPath.isEditable()) {
					textFieldPath.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldPath.setForeground(Color.LIGHT_GRAY);
					textFieldPath.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldPath.getText().toString().equals("")) {
					textFieldPath.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldPath.setForeground(Color.GRAY);
					textFieldPath.setText("C:/Users/name/Desktop/...");
				}
			}
		});
		textFieldPath.setColumns(10);
		textFieldPath.setBounds(711, 308, 240, 34);
		contentPane.add(textFieldPath);
		
	
	  
		
		JButton btnchooser = new JButton("");
		btnchooser.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/folder.png")));
		btnchooser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				fileChooser = new JFileChooser(); 
				fileChooser.setDialogTitle("Choose Directory");
	            fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
	            int option = fileChooser.showOpenDialog(btnchooser);
	            if(option == JFileChooser.APPROVE_OPTION){
	            	Folder_Selected = fileChooser.getSelectedFile().getAbsolutePath();
	            	textFieldPath.setText(Folder_Selected);
	            	textFieldPath.setForeground(Color.LIGHT_GRAY);
	            }else{
	            	Folder_Selected= "C:/Users/name/Desktop/...";
	            }
			}
		});
		btnchooser.setToolTipText("Path chooser");
		btnchooser.setBounds(961, 308, 34, 34);
		contentPane.add(btnchooser);
		
//Progress Bar ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////		

		JButton btnNewButton = new JButton("");
		btnNewButton.setToolTipText("GO to Training");
		btnNewButton.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				btnNewButton.setIcon(new ImageIcon(Datasets.class.getResource("/arrows/next selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				btnNewButton.setIcon(new ImageIcon(Datasets.class.getResource("/arrows/next.png")));
			}
		});
		btnNewButton.setIcon(new ImageIcon(Datasets.class.getResource("/arrows/next.png")));
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
			if (DataProcessed_==true && i!=1) {
				Training frame = new Training(dataset_,path_data,DataProcessed_);
				frame.setLocationRelativeTo(contentPane);
				frame.setVisible(true);
				dispose();
			}
			else {
				if (i==1) {
				String Path_save =textFieldPath.getText();
				Training frame = new Training(String.valueOf(dataset),Path_save,DataProcessed);
				frame.setLocationRelativeTo(contentPane);
				frame.setVisible(true);
				dispose();
				}
				else {
					JOptionPane.showMessageDialog(null,  "Please process a dataset !","Warning" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/error.png")));	
				}
				
			}
			}
		});
		btnNewButton.setBounds(296, 86, 32, 32);
		ButtonStyle(btnNewButton);
		contentPane.add(btnNewButton);
	   
		
		
//le background////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		BGDatasets.setBounds(0, 0, 1100, 650);
		contentPane.add(BGDatasets);
		
		
	}
//methode du style des buttons/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	 private void ButtonStyle(JButton btn) {
	//enlecer les bordures des btn
	 btn.setOpaque(false);
	 btn.setFocusPainted(false);
	 btn.setBorderPainted(false);
	 btn.setContentAreaFilled(false);
	
}	 
	 
	 
}
