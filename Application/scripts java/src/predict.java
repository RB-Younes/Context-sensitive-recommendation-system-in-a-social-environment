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
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

import javax.swing.ButtonGroup;
import javax.swing.DefaultComboBoxModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
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


////////////////////////////////////////////////////////////////////////////////-----------Fenetre Menu Medecin------------///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

public class predict extends JFrame {
	

	private static final long serialVersionUID = 1L;

	//protected static final String ID_Med = null;
	
	Connection cnx=null;
	PreparedStatement prepared = null;
	ResultSet resultat =null; 
	
	private int posX = 0;   //Position X de la souris au clic
    private int posY = 0;   //Position Y de la souris au clic
    

	private JPanel contentPane;
	
	private JButton btn1;
	private JTextField textFieldDistance;
	private JTextField textFieldTopK;
	
	
	
	private JComboBox<String> comboBoxCombiRatio ;
	private JCheckBox chckbxCombi ;
	private JComboBox<String> comboImpExpRatio;
	private JRadioButton RadiobtnJaccard ;
	private JRadioButton RadiobtnCosine; 
	private JCheckBox chckbxImpExpTrust;
	private JCheckBox chckbxContexte;
	private JRadioButton RadiobtnSeason;
	private JTextField textFieldSample;
	private JTextField textFieldTopKIPIT;

	
	

	/**
	 * Launch the application.
	 * @throws UnsupportedLookAndFeelException 
	 */
	public static void main(String[] args) throws UnsupportedLookAndFeelException {
		FlatDarculaLaf.install();	
		UIManager.setLookAndFeel(new FlatDarculaLaf() );
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					predict frame = new predict("1","C:/Users/LATITUDE/Desktop/Chapitre 2/","C:/Users/LATITUDE/Desktop/Chapitre 2/",true,"2");
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
	public predict(String dataset,String path_data,String model_path,Boolean DataProcessed,String C_model) {
		setIconImage(Toolkit.getDefaultToolkit().getImage(predict.class.getResource("/Menu_img/train.png")));
		//cnx

		setUndecorated(true);	
		setResizable(false);

		setTitle("Prediction");
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
		//BGDatasets.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/1.png")));	// Back ground de base	
       
// Bouton Reduire ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton Minimise_BTN = new JButton("");
		Minimise_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(predict.class.getResource("/Menu_img/Minimize ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(predict.class.getResource("/Menu_img/Minimize ML .png")));
			}
		});
		Minimise_BTN.setToolTipText("Minimize");
		ButtonStyle(Minimise_BTN);
		Minimise_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setState(ICONIFIED);
				
			}
		});
		Minimise_BTN.setIcon(new ImageIcon(predict.class.getResource("/Menu_img/Minimize ML .png")));
		Minimise_BTN.setBounds(932, 11, 32, 32);
		contentPane.add(Minimise_BTN);
//Boutton home//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				JButton btnHome = new JButton("");
				btnHome.addMouseListener(new MouseAdapter() {
					@Override
					public void mouseEntered(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(predict.class.getResource("/Models_img/home selected.png")));//changer les couleurs button
						}
					}
					@Override
					public void mouseExited(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(predict.class.getResource("/Models_img/home.png")));//remetre le bouton de base
						}
					}
				});
				btnHome.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						Menu frame = new Menu(dataset,path_data,DataProcessed);
						frame.setLocationRelativeTo(null);
						frame.setVisible(true);
						dispose();
					}
				});
				btnHome.setIcon(new ImageIcon(predict.class.getResource("/Models_img/home.png")));
				btnHome.setToolTipText("Menu");
				btnHome.setBounds(974, 11, 32, 32);
				ButtonStyle(btnHome);
				contentPane.add(btnHome);
// Exit bouton//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		JButton Exit_BTN = new JButton("");
		Exit_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(predict.class.getResource("/Menu_img/Exit ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(predict.class.getResource("/Menu_img/Exit ML.png")));
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
		Exit_BTN.setIcon(new ImageIcon(predict.class.getResource("/Menu_img/Exit ML.png")));
		Exit_BTN.setBounds(1016, 11, 32, 32);
		contentPane.add(Exit_BTN);
//btns ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		btn1= new JButton("");
		btn1.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
					if(dataset.equals("3"))
						BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/Film trust (2).png")));
					else {
						if(dataset.equals("2") )
							BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/yelp (2).png")));
						else
							BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/ML-1M (2).png")));
					}
					
			}
			@Override
			public void mouseExited(MouseEvent e) {
					if(dataset.equals("3") )
						BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/Film trust.png")));
					else {
						if(dataset.equals("2") )
							BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/yelp.png")));
						else
							BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/ML-1M.png")));
					}
			}
		});
		btn1.setToolTipText("Predict and show result");
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
									if(dataset.equals("3")) { //Film Trust
										
													String  test_path = path_data;//--
													String  model_p = model_path;//--
													String  users_sample = null;//--
													String 	Alpha_it_et = null;//--
													String  Alpha_combi = null;
													String  k = null;//--
													String it_et_bool = null;//--
													String  combination_bool = null;//--
													
													
													users_sample =textFieldSample.getText();
													Alpha_it_et  =(String) comboImpExpRatio.getSelectedItem();
													k = textFieldTopKIPIT.getText();
													Alpha_combi =(String) comboBoxCombiRatio.getSelectedItem();
													
													if (path_data.equals("C:/Users/name/Desktop/...")) {
														test_path="C:/users/" + System.getProperty("user.name") + "/Desktop/";
													}
													else {
														test_path =path_data+'\\';
													}
													if (model_path.equals("C:/Users/name/Desktop/...")) {
														model_p="C:/users/" + System.getProperty("user.name") + "/Desktop/";
													}
													else {
														model_p =model_path+'\\';
													}
													
													if (chckbxImpExpTrust.isSelected()) {
														it_et_bool="1";
													}
													else {
														it_et_bool="-1";
													}
													if (Alpha_it_et.equals("Choose")) {
														Alpha_it_et="0.5";
													}
													
													
													if (k.equals("1 , 2 ...")) {
														k="5";
													}
													
													if (chckbxCombi.isSelected()) {
														combination_bool="1";
													}
													else {
														combination_bool="-1";
													}
													if (Alpha_combi.equals("Choose")) {
														Alpha_combi="0.5";
													}
													
													if (users_sample.equals("1 , 2 ...")) {
														users_sample="10";
													}
													
										String path_script ="";
										path_script = test.class.getResource("/scripts_py/FilmTrust_Prediction.py").getPath(); // get the path of the script (a revoir)
										path_script = path_script.substring(1, path_script.length());
										ProcessBuilder pb = new ProcessBuilder("python",path_script,
												"--test_path",test_path,"--model_path",model_p,"--users_sample",users_sample,"--Alpha_it_et",Alpha_it_et,"--Alpha_combi",Alpha_combi,
												"--k",k,"--it_et_bool",it_et_bool,"--combination_bool",combination_bool).inheritIO();
										try {
											 process=pb.start();
											try {
												 process.waitFor();
											} catch (InterruptedException e1) {
												// TODO Auto-generated catch block
												e1.printStackTrace();
											}
											
											} catch (IOException e) {
												// TODO Auto-generated catch block
												JOptionPane.showMessageDialog(null,e);
											}
									}
									if(dataset.equals("1")) { //ML-1M
										
						    
									    String  path_test = path_data;//--
										String  model_p = model_path;//--
										String  users_sample = null;//--
										String  Choice_model = C_model;
										String  Context_choice = null;//--
										
										users_sample =textFieldSample.getText();
										
										if (path_data.equals("C:/Users/name/Desktop/...")) {
											path_test="C:/users/" + System.getProperty("user.name") + "/Desktop/";
										}
										else {
											path_test =path_data+'\\';
										}
										if (model_path.equals("C:/Users/name/Desktop/...")) {
											model_p="C:/users/" + System.getProperty("user.name") + "/Desktop/";
										}
										else {
											model_p =path_data+'\\';
										}
										
										if (users_sample.equals("1 , 2 ...")) {
											users_sample="10";
										}
										if (chckbxContexte.isSelected()) {
											Context_choice ="1";
										}
										else {
											Context_choice ="-1";
										}
										String path_script ="";
										path_script = test.class.getResource("/scripts_py/ML-1M_Prediction.py").getPath(); // get the path of the script (a revoir)
										path_script = path_script.substring(1, path_script.length());
										
										ProcessBuilder pb = new ProcessBuilder("python",path_script,
												"--path_test",path_test,"--model_path",model_p,"--users_sample",users_sample,"--Choice_model",Choice_model,"--Context_choice",Context_choice).inheritIO();
										try {
											 process=pb.start();
											try {
												 process.waitFor();
											} catch (InterruptedException e1) {
												// TODO Auto-generated catch block
												e1.printStackTrace();
											}
											
											} catch (IOException e) {
												// TODO Auto-generated catch block
												JOptionPane.showMessageDialog(null,e);
											}	
									}
									
									if(dataset.equals("2")) { //Yelp
										
										String  test_path = path_data;//--
										String  model_p = model_path;//--
										String  users_sample = null;//--
										String  Choice_model = C_model;//--
										String  Alpha_combi = null;//--
										String  Context_choice = null;//--
										String  k = null;//--
										String  combination_bool = null;//--
										String  distance = null;
										String  Mode = null;
										
										
										users_sample =textFieldSample.getText();
										distance = textFieldDistance.getText();
										k = textFieldTopKIPIT.getText();
										Alpha_combi =(String) comboBoxCombiRatio.getSelectedItem();
										
										if (path_data.equals("C:/Users/name/Desktop/...")) {
											test_path="C:/users/" + System.getProperty("user.name") + "/Desktop/";
										}
										else {
											test_path =path_data+'\\';
										}
										if (model_path.equals("C:/Users/name/Desktop/...")) {
											model_p="C:/users/" + System.getProperty("user.name") + "/Desktop/";
										}
										else {
											model_p =path_data+'\\';
										}
										
										if (users_sample.equals("1 , 2 ...")) {
											users_sample="10";
										}
										if (chckbxContexte.isSelected()) {
											Context_choice ="1";
										}
										else {
											Context_choice ="-1";
										}
										if (distance.equals("1 , 2 ...")) {
											distance="20";
										}
										if (chckbxCombi.isSelected()) {
											combination_bool="1";
										}
										else {
											combination_bool="-1";
										}
										if (Alpha_combi.equals("Choose")) {
											Alpha_combi="0.5";
										}
										if(RadiobtnJaccard.isSelected()) {
											Mode="1";
										}
										else {
											if(RadiobtnCosine.isSelected()) {
												Mode="2";
											}
											else {
												Mode="1";
											}
										}
					
										if (k.equals("1 , 2 ...")) {
											k="5";
										}
										
										String path_script ="";
										path_script = test.class.getResource("/scripts_py/Yelp_Prediction.py").getPath(); // get the path of the script (a revoir)
										path_script = path_script.substring(1, path_script.length());
										
										ProcessBuilder pb = new ProcessBuilder("python",path_script,
												"--test_path",test_path,"--model_path",model_p,"--users_sample",users_sample,"--Choice_model",Choice_model,"--users_sample",users_sample,"--Choice_model",Choice_model,
												"--Alpha_combi",Alpha_combi,"--Context_choice",Context_choice,"--K",k,"--combination_bool",combination_bool,"--distance",distance,"--Mode",Mode).inheritIO();
										try {
											process=pb.start();
											try {
												 process.waitFor();
											} catch (InterruptedException e1) {
												// TODO Auto-generated catch block
												e1.printStackTrace();
											}
											
											} catch (IOException e) {
												// TODO Auto-generated catch block
												JOptionPane.showMessageDialog(null,e);
											}	
										
									}
									if(!stopped) {
										f.dispose();
										JOptionPane.showMessageDialog(null,  "Completed processing !","state" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/stamp.png")));	
										/*String path_res = test.class.getResource("/scripts_py/P-r-e-s/result.png").getPath();
										File file = new File(path_res);
								        
								        //first check if Desktop is supported by Platform or not
								        if(!Desktop.isDesktopSupported()){
								            return;
								        }
								        
								        Desktop desktop = Desktop.getDesktop();
								        if(file.exists())
											try {
												desktop.open(file);
											} catch (IOException e) {
												// TODO Auto-generated catch block
												e.printStackTrace();
											} */   
									}
					                else {
					                	f.dispose();
										JOptionPane.showMessageDialog(null,  "Stopped treatment.","state" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/error.png")));	
										stopped=false;
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
								BG.setIcon(new ImageIcon(Datasets.class.getResource("/predict_img/process Prediction.png")));
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
		btn1.setBounds(782, 395, 215, 44);
		ButtonStyle(btn1);
		contentPane.add(btn1);
//radio btns//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
		RadiobtnJaccard = new JRadioButton("");
		RadiobtnJaccard.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
				if (RadiobtnJaccard.isSelected()) {
					textFieldTopK.setEnabled(true);
				}
			else {
				textFieldTopK.setEnabled(false);
				textFieldTopK.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
				textFieldTopK.setForeground(Color.GRAY);
				textFieldTopK.setText("1 , 2 ...");
				}
			}
		});
		RadiobtnJaccard.setToolTipText("Jaccard similarity");
		RadiobtnJaccard.setBounds(455, 362, 21, 23);
		contentPane.add(RadiobtnJaccard);
		
		RadiobtnCosine = new JRadioButton("");
		RadiobtnCosine.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
				if (RadiobtnCosine.isSelected()) {
					textFieldTopK.setEnabled(true);
				}
			else {
				textFieldTopK.setEnabled(false);
				textFieldTopK.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
				textFieldTopK.setForeground(Color.GRAY);
				textFieldTopK.setText("1 , 2 ...");
				}
			}
		});
		RadiobtnCosine.setToolTipText("Cosine similarity");
		RadiobtnCosine.setBounds(455, 404, 21, 23);
		contentPane.add(RadiobtnCosine);
		if(dataset.equals("3")) RadiobtnCosine.setEnabled(false);
		
		
		   //Group the radio buttons.
		ButtonGroup group = new ButtonGroup();
		group.add(RadiobtnJaccard);
		group.add(RadiobtnCosine);
		
		textFieldDistance = new JTextField();
		textFieldDistance.setEnabled(false);
		textFieldDistance.setToolTipText("MLP Batch size");
		textFieldDistance.setText("1 , 2 ...");
		textFieldDistance.setForeground(Color.GRAY);
		textFieldDistance.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldDistance.addKeyListener(new KeyAdapter() {
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
		textFieldDistance.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldDistance.getText().toString().equals("1 , 2 ...")) {
					textFieldDistance.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldDistance.setForeground(Color.LIGHT_GRAY);
					textFieldDistance.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldDistance.getText().toString().equals("")) {
					textFieldDistance.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldDistance.setForeground(Color.GRAY);
					textFieldDistance.setText("1 , 2 ...");
				}
			}
		});
		textFieldDistance.setColumns(10);
		textFieldDistance.setBounds(206, 395, 78, 32);
		contentPane.add(textFieldDistance);
		
		comboImpExpRatio = new JComboBox<String>();
		comboImpExpRatio.setEnabled(false);
		comboImpExpRatio.setToolTipText("HybMLP Number of predictive factors");
		comboImpExpRatio.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"} ));
		comboImpExpRatio.setBounds(525, 275, 96, 32);
		contentPane.add(comboImpExpRatio);
		
		textFieldTopK = new JTextField();
		textFieldTopK.setEnabled(false);
		textFieldTopK.setToolTipText("Top K similar persons");
		textFieldTopK.setText("1 , 2 ...");
		textFieldTopK.addKeyListener(new KeyAdapter() {
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
		textFieldTopK.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldTopK.getText().toString().equals("1 , 2 ...")) {
					textFieldTopK.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldTopK.setForeground(Color.LIGHT_GRAY);
					textFieldTopK.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldTopK.getText().toString().equals("")) {
					textFieldTopK.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldTopK.setForeground(Color.GRAY);
					textFieldTopK.setText("1 , 2 ...");
				}
			}
		});
		textFieldTopK.setForeground(Color.GRAY);
		textFieldTopK.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldTopK.setColumns(10);
		textFieldTopK.setBounds(520, 445, 78, 32);
		contentPane.add(textFieldTopK);
		
		comboBoxCombiRatio = new JComboBox<String>();
		comboBoxCombiRatio.setEnabled(false);
		comboBoxCombiRatio.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"} ));
		comboBoxCombiRatio.setToolTipText("HybMLP Embedding size");
		comboBoxCombiRatio.setBounds(847, 273, 96, 32);
		contentPane.add(comboBoxCombiRatio);
//Early stopping Patience/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		chckbxCombi = new JCheckBox("");
		chckbxCombi.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
				if (chckbxCombi.isSelected()) {
					comboBoxCombiRatio.setEnabled(true);
				}
			else {
				comboBoxCombiRatio.setEnabled(false);
				comboBoxCombiRatio.setSelectedIndex(0);
				}
			}
		});
		chckbxCombi.setToolTipText("combination between colaborativ filtring & social Filtring");
		chckbxCombi.setBounds(782, 202, 21, 23);
		contentPane.add(chckbxCombi);
		
		
		JButton btnNewButton = new JButton("");
		btnNewButton.setToolTipText("GO to datasets");
		btnNewButton.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				btnNewButton.setIcon(new ImageIcon(Datasets.class.getResource("/arrows/previous selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				btnNewButton.setIcon(new ImageIcon(Datasets.class.getResource("/arrows/previous.png")));
			}
		});
		btnNewButton.setIcon(new ImageIcon(predict.class.getResource("/arrows/previous.png")));
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				Datasets frame = new Datasets(dataset,path_data,DataProcessed);
				frame.setLocationRelativeTo(contentPane);
				frame.setVisible(true);
				dispose();
			}
		});
		btnNewButton.setBounds(295, 87, 32, 32);
		ButtonStyle(btnNewButton);
		contentPane.add(btnNewButton);
		
		chckbxImpExpTrust = new JCheckBox("");
		chckbxImpExpTrust.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
				if (chckbxImpExpTrust.isSelected()) {
					comboImpExpRatio.setEnabled(true);
					textFieldTopKIPIT.setEnabled(true);
				}
			else {
				comboImpExpRatio.setEnabled(false);
				comboImpExpRatio.setSelectedIndex(0);
				textFieldTopKIPIT.setEnabled(false);
				textFieldTopKIPIT.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
				textFieldTopKIPIT.setForeground(Color.GRAY);
				textFieldTopKIPIT.setText("1 , 2 ...");
				
				}
			}
		});
		chckbxImpExpTrust.setToolTipText("Implicit and explicit trust");
		chckbxImpExpTrust.setBounds(500, 190, 21, 23);
		contentPane.add(chckbxImpExpTrust);
		
		chckbxContexte = new JCheckBox("");
		chckbxContexte.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
				if (chckbxContexte.isSelected()) {
					if(dataset.equals("2") ) 
						textFieldDistance.setEnabled(true);
					if(dataset.equals("1") ) {
						RadiobtnSeason.setEnabled(true);
						RadiobtnSeason.setSelected(true);
					}
				}
			else {
				if(dataset.equals("2") ) {
				textFieldDistance.setEnabled(false);
				textFieldDistance.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
				textFieldDistance.setForeground(Color.GRAY);
				textFieldDistance.setText("1 , 2 ...");}
				if(dataset.equals("1") ) {
					RadiobtnSeason.setEnabled(false);
					RadiobtnSeason.setSelected(false);
				}
				}
			}
		});
		chckbxContexte.setToolTipText("Early stopping");
		chckbxContexte.setBounds(150, 350, 21, 23);
		contentPane.add(chckbxContexte);
		
		RadiobtnSeason = new JRadioButton("");
		RadiobtnSeason.setEnabled(false);
		RadiobtnSeason.setToolTipText("HybMLP");
		RadiobtnSeason.setBounds(150, 457, 21, 23);
		contentPane.add(RadiobtnSeason);
		
		
//le background////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		if(dataset.equals("3")) {
			BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/Film trust.png")));
			RadiobtnJaccard.setEnabled(false);
			RadiobtnCosine.setEnabled(false);
			chckbxContexte.setEnabled(false);
		}
		else { 
				if(dataset.equals("1") ) {
					BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/ML-1M.png")));
					RadiobtnJaccard.setEnabled(false);
					RadiobtnCosine.setEnabled(false);
					chckbxImpExpTrust.setEnabled(false);
					comboImpExpRatio.setEnabled(false);
					chckbxCombi.setEnabled(false);
				}
				else {
					BGDatasets.setIcon(new ImageIcon(predict.class.getResource("/predict_img/yelp.png")));
					chckbxImpExpTrust.setEnabled(false);
					comboImpExpRatio.setEnabled(false);
					RadiobtnSeason.setEnabled(false);
				}
			  }
		
		textFieldSample = new JTextField();
		textFieldSample.setToolTipText("size of sample");
		textFieldSample.setText("1 , 2 ...");
		textFieldSample.setForeground(Color.GRAY);
		textFieldSample.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldSample.addKeyListener(new KeyAdapter() {
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
		textFieldSample.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldSample.getText().toString().equals("1 , 2 ...")) {
					textFieldSample.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldSample.setForeground(Color.LIGHT_GRAY);
					textFieldSample.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldSample.getText().toString().equals("")) {
					textFieldSample.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldSample.setForeground(Color.GRAY);
					textFieldSample.setText("1 , 2 ...");
				}
			}
		});
		textFieldSample.setColumns(10);
		textFieldSample.setBounds(206, 216, 78, 32);
		contentPane.add(textFieldSample);
		
		textFieldTopKIPIT = new JTextField();
		textFieldTopKIPIT.setToolTipText("Top K similar persons");
		textFieldTopKIPIT.setText("1 , 2 ...");
		textFieldTopKIPIT.setForeground(Color.GRAY);
		textFieldTopKIPIT.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldTopKIPIT.setEnabled(false);
		textFieldTopKIPIT.addKeyListener(new KeyAdapter() {
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
		textFieldTopKIPIT.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldTopKIPIT.getText().toString().equals("1 , 2 ...")) {
					textFieldTopKIPIT.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldTopKIPIT.setForeground(Color.LIGHT_GRAY);
					textFieldTopKIPIT.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldTopKIPIT.getText().toString().equals("")) {
					textFieldTopKIPIT.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldTopKIPIT.setForeground(Color.GRAY);
					textFieldTopKIPIT.setText("1 , 2 ...");
				}
			}
		});
		textFieldTopKIPIT.setColumns(10);
		textFieldTopKIPIT.setBounds(525, 232, 78, 32);
		contentPane.add(textFieldTopKIPIT);
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
