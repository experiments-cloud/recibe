(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (ontable b)
    (ontable a)
    (ontable c)
    (ontable e)
    (ontable d)
    (clear d)
    (handempty)
    (on e c)
    (on c a)
    (on a b)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
